# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from django.contrib.auth import  logout as django_logout, authenticate, login as django_login
from django.views.generic import View

from users.forms import LoginForm


class LoginView(View):
    # Create your views here.
    def post(self, request):
        error_massages =[]
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usr')
            password = form.cleaned_data.get('pwd')
            user = authenticate(username=username, password = password)
            if user is None:
                error_massages.append("Nombre de usuario o contraseña incorrecta")
            else:
                if user.is_active:
                    django_login(request,user)
                    url=request.GET.get('next','photos_home')
                    return redirect(url)
                else:
                    error_massages.append("El usuario no esta activo")

        context = {
            'errors': error_massages,
            'login_form': form
        }
        return  render(request, 'users/login.html', context)

    def get(self,request):
        form = LoginForm()
        error_massages =[]
        context = {
            'errors': error_massages,
            'login_form': form
        }
        return render(request, 'users/login.html', context)

class LogoutView(View):

    def get(self, request):
        if request.user.is_authenticated():
            django_logout(request)
        return redirect('photos_home')
