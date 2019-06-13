from django.contrib import admin
from django.urls import path,include

from sitetest.views import index, consumo, model_form_upload, printer, pdf

app_name = 'sitetest'

urlpatterns = [
    path('', index, name='site_index'),
    path('<int:cliente_id>/consumo', consumo, name='consumo'),
    path('carga/', model_form_upload, name='carga'),
    path('printer/', printer, name='printer'),
    path('pdf/', pdf, name='pdf'),
]

