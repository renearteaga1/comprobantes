from django.db import models
from django.db.models.signals import post_delete, pre_delete
from django.contrib.auth.models import User

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>

    return '{0}/{1}/{2}'.format(instance.tipo, instance.anio, filename)

def oficio_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}/{2}/{3}'.format(instance.tipo, instance.institucion, instance.anio, filename)

class ConteoComprobante(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    conteo = models.IntegerField()
    errores = models.IntegerField(default=0)
    tipo_documento = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.uploaded_date.strftime('%m/%d/%Y')

class ErrorCarga(models.Model):
    conteo_id = models.ForeignKey(ConteoComprobante, on_delete=models.DO_NOTHING)
    archivo = models.CharField(max_length=255, blank=True, null=True, default='Sin error')
    tipo_error = models.CharField(max_length=255, blank=True, null=True)
    tipo_documento = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.archivo

class Comprobante(models.Model):
    descripcion = models.CharField(max_length=255, blank=True)
    numero_comprobante = models.IntegerField(blank=False, null=False)
    archivo = models.FileField(upload_to=user_directory_path)
    tipo = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    anio = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    conteo_id = models.ForeignKey(ConteoComprobante, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.descripcion

    def delete(self, *args, **kwargs):
        self.archivo.delete()
        super().delete(*args, **kwargs)

class Oficio(models.Model):
    descripcion = models.CharField(max_length=255, blank=True)
    archivo = models.FileField(upload_to=oficio_directory_path)
    tipo = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    anio = models.IntegerField(blank=True, null=True)
    institucion = models.CharField(max_length=255)
    respuesta = models.CharField(max_length=255)
    entrante = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    conteo_id = models.ForeignKey(ConteoComprobante, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.descripcion

    def delete(self, *args, **kwargs):
        self.archivo.delete()
        super().delete(*args, **kwargs)

def del_comprobantes(sender, instance, **kwargs):
    print('Deleted')
    conteo_comprobante = instance.conteo_id
    print(conteo_comprobante)
    conteo_comprobante.conteo = conteo_comprobante.conteo - 1
    conteo_comprobante.save()


post_delete.connect(del_comprobantes, sender=Comprobante)

post_delete.connect(del_comprobantes, sender=Oficio)

def del_files(sender, instance, **kwargs):
    instance.archivo.delete()

def del_files_oficio(sender, instance, **kwargs):
    instance.archivo.delete()

pre_delete.connect(del_files, sender=Comprobante)

pre_delete.connect(del_files_oficio, sender=Oficio)
