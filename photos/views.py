from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from frikr.settings import LOGIN_URL
from photos.models import Photo, PUBLIC
from photos.forms import PhotoForm
from  django.contrib.auth.decorators import login_required
from django.db.models import  Q
# Create your views here.

class  PhotosQueryset(object):
    def get_photos_queryset(self,request):
        if not request.user.is_authenticated():
            photos = Photo.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser:
            photos = Photo.objects.all()
        else:
            photos = Photo.objects.filter(Q(owner=request.user) | Q(visibility=PUBLIC))
        return photos

class HomeView(View):
    def get(self, request):
        photos = Photo.objects.filter(visibility=PUBLIC).order_by('-created_at')
        #html = '<ul>'
        #for photo in photos:
        #   html += '<li>'+photo.name+'</li>'
        #html+='</ul>'
        context={
            "photos_list": photos[:5]
        }
        return render(request,'photos/home.html',context)


class DetailView(View, PhotosQueryset):
    def get(self, request, pk):
        """
        Carga la pagina de detalle de una foto
        :param request: HttpRequest
        :param pk: id de la foto
        :return: HttpResponse
        """
        possible_photos = self.get_photos_queryset(request).filter(pk=pk).select_related('owner')  #utilizar pk siempre va a buscar por el valor que sea clave primaria
        if len(possible_photos) == 1:
            photo = possible_photos[0]
        else:
            photo = None

        if photo is not None:
            #cargamos la plantilla detalle
            context ={
                'photo': photo
            }
            return render(request, 'photos/detail.html', context)
        else:
            return  HttpResponse('No existe esta foto') #404 Not found


class CreateView(View):

    @method_decorator(login_required())
    def post(self,request):
        """
        Muestra un formulario para crear una foto y la crea si la peticion es POST
        :param request:
        :return:
        """
        success_mesage= ''
        photo_with_owner = Photo()
        photo_with_owner.owner = request.user
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
               new_photo = form.save() #Guarda el objeto foto y se lo devuelve
               form = PhotoForm()
               success_mesage = 'Guardado con exito '
               success_mesage += '<a href="{0}">'.format(reverse('photo_detail', args=[new_photo.pk]))
               success_mesage += 'Ver foto'
               success_mesage += '</a>'

        context = {
            'form': form,
            'success_message': success_mesage
        }
        return render(request,'photos/new.html', context)

    @method_decorator(login_required())
    def get(self,request):
        success_mesage= ''
        form = PhotoForm()
        context = {
            'form': form,
            'success_message': success_mesage
        }
        return render(request, 'photos/new.html', context)

class ListView(View, PhotosQueryset):

    def __get__(self, request):
        """
        Devuelve fotos p
        :param request:
        :return:
        """
        context = {
            'photos': self.get_photos_queryset(request)
        }
        return render(request, 'photos/photos_list.html', context)