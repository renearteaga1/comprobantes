from django.contrib import admin

from .models import Comprobante, ConteoComprobante, ErrorCarga, Oficio

# Register your models here.
class ConteoComprobanteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'conteo', 'uploaded_date')

class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'tipo','anio')

admin.site.register(Comprobante, ComprobanteAdmin)
admin.site.register(ConteoComprobante, ConteoComprobanteAdmin)
admin.site.register(ErrorCarga)
admin.site.register(Oficio)
