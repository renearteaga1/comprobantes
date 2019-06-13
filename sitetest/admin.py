from django.contrib import admin

from .models import Producto, Proveedor, Cliente, Credito, Factura, Consumo

# Register your models here.
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Credito)
admin.site.register(Factura)
admin.site.register(Consumo)

