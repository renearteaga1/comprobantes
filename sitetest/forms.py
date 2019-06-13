from django import forms

from .models import Cliente, Credito, Producto
#from uploads.core.models import Document


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Credito
        fields = ['cliente', 'cupo', 'saldo', 'activo']
        widgets = {
            # 'nombre':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            # 'codigo':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            # 'costo':forms.NumberInput(attrs={'class':'form-control form-control-sm'}),
            # 'precio':forms.NumberInput(attrs={'class':'form-control form-control-sm'}),
            # 'proveedor':forms.Select(attrs={'class':'form-control form-control-sm'})
        }


def proveedor_choices():
    choice_list = Proveedor.objects.all()
    #choice_list = (('10','10'),('20','20'))
    return choice_list

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'ruc']

#class DocumentForm(forms.ModelForm):
#    class Meta:
#        model = Document
#        fields = ('description', 'document', )
