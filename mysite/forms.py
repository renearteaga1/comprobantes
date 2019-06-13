from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=("Usuario"),max_length=254, widget=forms.TextInput(attrs={"class":"form-control col-md-3","placeholder":"Usuario"}))
    password = forms.CharField(label=("Contrasena"), widget=forms.PasswordInput(attrs={"class":"form-control col-md-3","placeholder":"Contrasena"}))
