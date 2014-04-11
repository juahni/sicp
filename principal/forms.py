# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="usuario"
__date__ ="$11-04-2014 12:11:33 PM$"

import re
from django import forms
from django.contrib.auth.models import User
from principal.models import *

# Create the form class.

# Formularios para los USUARIOS.

class RegistrationForm(forms.Form):
    
    #Formulario para registrar un nuevo usuario. 

    username = forms.CharField(label=u'Nombre de usuario', max_length=30)
    nombre = forms.CharField(label=u'Nombre', max_length=30)
    apellido = forms.CharField(label=u'Apellido', max_length=30)
    ci = forms.IntegerField(label=u'Cedula de identidad', required=False)
    direccion = forms.CharField(label=u'Direccion', max_length=200, required=False)
    telefono = forms.CharField(label=u'Telefono', max_length=15, required=False)
    email = forms.EmailField(label=u'Email', required=False)
    password1 = forms.CharField(label=u'Contrasena', widget=forms.PasswordInput())
    password2 = forms.CharField(label=u'Confirmar Contrasena', widget=forms.PasswordInput())

    #Verificacion de la contrasenha
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Las contrasenas no coinciden')
    
    #Verificacion del nombre de usuario.
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            if bool(User.objects.get(username=username)):
                raise forms.ValidationError('El nombre de usuario ya existe o ya fue utilizado por un usuario que se ha borrado.')
        except User.DoesNotExist:
            return username

class ModificarUserForm(forms.Form):
    """Formulario para la modificacion de los datos de un usuario."""

    nombre = forms.CharField(label=u'Nombre', max_length=30)
    apellido = forms.CharField(label=u'Apellido', max_length=30)
    ci = forms.IntegerField(label=u'Cedula de identidad', required=False)
    direccion = forms.CharField(label=u'Direccion', max_length=200, required=False)
    telefono = forms.CharField(label=u'Telefono', max_length=15, required=False)
    email = forms.EmailField(label=u'Email', required=False)

class CambiarContrasenaForm(forms.Form):
    """
    Formulario para el cambio de la contrasenha de un usuario. Incluye una
    funcion para la verificacion de la contrasenha.

    """

    username = forms.CharField(label=u'Nombre de usuario', max_length=30)
    password = forms.CharField(label=u'Contrasena', widget=forms.PasswordInput())
    password1 = forms.CharField(label=u'Nueva Contrasena', widget=forms.PasswordInput())
    password2 = forms.CharField(label=u'Confirmar Contrasena', widget=forms.PasswordInput())

    #Verifica la contrasenha anterior
    def clean_password(self):
        if 'password' in self.cleaned_data:
            user = User.objects.get(username=self.cleaned_data['username'])
            password = self.cleaned_data['password']
            if user.check_password(password):
                return password
        raise forms.ValidationError('La contrasena no es valida')

    #Verifica la contrasenha nueva con la que se confirma
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Las contrasenas no coinciden')
