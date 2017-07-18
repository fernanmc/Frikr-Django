# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from photos.models import   Photo
from photos.settings import BADWORDS


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        exclude = ['owner']
    def clean(self):
        """
        Valida si en la descripcion se han puesto tacos definidos en settings.BADWORDS
        :return: diccionario con los atributos si OK
        """
        cleaned_data = super(PhotoForm,self).clean()
        description = cleaned_data.get('description','').lower()

        for badword in BADWORDS:
            if badword.lower() in description:
                raise ValidationError(u'La palabra {0} no está permitida'.format(badword))

        # si va ok devuelve los datos normalizados
        return  cleaned_data
