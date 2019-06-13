from django.contrib import admin
from django.urls import path,include

from cargar.views import update, model_form_upload, ajax_cargar, comprobante_list, reporte, reporte_errores, eliminar, eliminar_carpeta, delete_folder, carpeta, carpeta_oficio, busqueda, login_view, password_reset, logout_view

app_name = 'cargar'

urlpatterns = [
    path('', comprobante_list, name='lista'),
    path('update/', update, name='update'),
    path('carga/', model_form_upload, name='index'),
    path('ajax_cargar/', ajax_cargar, name='ajax_cargar'),
    path('lista/', comprobante_list, name='comprobante_list'),
    path('eliminar/<int:pk>/', eliminar, name='comprobante_eliminar'),
    #path('nueva-carpeta/<int:y>/', nueva_carpeta, name='nueva_carpeta'),
    path('eliminarcarpeta/',  delete_folder, name='delete_folder'),
    path('<slug:slug>/eliminar',  eliminar_carpeta, name='eliminar_carpeta'),
    path('carpeta/', carpeta, name='carpeta'),
    path('carpetaoficio/', carpeta_oficio, name='carpeta_oficio'),
    path('busqueda/',  busqueda, name='busqueda'),
    path('reporte/', reporte, name='reporte'),
    path('reporte/<int:pk>/', reporte_errores, name='reporte_errores'),
    #path('login/',  login_view, name='login'),
    path('logout/',  logout_view, name='logout'),
    path('reset/',  password_reset, name='password_reset'),

]
