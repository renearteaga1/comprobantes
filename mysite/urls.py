"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .forms import CustomAuthenticationForm

urlpatterns = [
    path('', include('cargar.urls', namespace='cargar')),
    path('admin/', admin.site.urls),
    path('test/', include('sitetest.urls',namespace='sitetest')),
    path('cargar/', include('cargar.urls',namespace='cargar')),
    path('subir/', include('subir.urls',namespace='subir')),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm,redirect_field_name='cargar:index'), name='login'),
]

#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
