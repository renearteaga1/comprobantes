import os
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

#from .models import Comprobante
from .models import Comprobante



class ComprobanteForm(forms.ModelForm):
    # path = '/home/nick/Documents/Django_Stuff/projectone/mysite/media/Comprobantes'
    # files = os.listdir(path)
    # i = 1
    # path_1 = settings.MEDIA_ROOT
    # path = os.path.join(path, 'Comprobantes')
    # Choices = [("","Seleccionar Carpeta")]
    # for carpeta in files:
    #         Choices.append((carpeta, carpeta))

    #anio = forms.ChoiceField(choices=Choices)
    class Meta:
        model = Comprobante
        #fields = ['anio', 'comprobante']
        fields = ['archivo']
        widgets = {
            'archivo':forms.ClearableFileInput(attrs={'multiple': True,}),
            # 'nombre':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            # 'codigo':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            # 'costo':forms.NumberInput(attrs={'class':'form-control form-control-sm'}),
            # 'precio':forms.NumberInput(attrs={'class':'form-control form-control-sm'}),
            # 'proveedor':forms.Select(attrs={'class':'form-control form-control-sm'})
        }

# path = '/home/nick/Documents/Django_Stuff/projectone/mysite/media/Comprobantes'
# files = os.listdir(path)
# i = 1
# Choices = [("","Seleccionar Carpeta")]
# for carpeta in files:
#         Choices.append((carpeta, carpeta))

# class ComprobanteCarpetaForm(ComprobanteForm):
#     carpeta_anio = forms.ChoiceField(choices=Choices)
#
#     class Meta(ComprobanteForm.Meta):
#         fields = ComprobanteForm.Meta.fields + ['carpeta_anio']


class CrearCarpetaForm(forms.Form):
    #anio = forms.IntegerField()
    nombre_carpeta = forms.CharField(widget=forms.TextInput)

class AuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
