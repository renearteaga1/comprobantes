from django.db import models

from django.db.models.signals import post_save

from django.core.validators import RegexValidator

# Create your models here.
# class Proveedor(models.Model):
#     nombre = models.CharField(max_length=150, blank=False)
#     codigo = models.CharField(max_length=15, blank=False, unique=True)
#     ruc = models.BigIntegerField(max_length=13)
#     def __str__(self):
#         return self.nombre


cuenta_choice = (
    ('cuenta_ahorros', 'Cuenta Ahorros'),
    ('cuenta_corriente', 'Cuenta Corriente')
)

banco_choice = (
    ()
)

class Proveedor(models.Model):
    class Meta:
        verbose_name_plural = 'proveedores'
    razon_social = models.CharField(max_length=150, blank=False)
    ruc = models.BigIntegerField(validators=[RegexValidator(r'^[1-9]\d{9}$|^[1-9]\d{12}$')], unique=True)
    direccion = models.CharField(max_length=265, blank=True)
    correo = models.EmailField(max_length=50, blank=True, null=True)
    telefono = models.BigIntegerField(blank=True, null=True)
    banco = models.CharField(max_length=50, blank=True, null=True)
    tipo_cuenta = models.CharField(max_length=25, choices=cuenta_choice, blank=True, null=True)
    numero_cuenta = models.BigIntegerField(blank=True, null=True)
    vendedor = models.CharField(max_length=150, blank=True, null=True)
    vendedor_telefono = models.BigIntegerField(blank=True, null=True)
    vendedor_correo = models.EmailField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.razon_social

class Producto(models.Model):
    nombre = models.CharField(max_length=150, blank=False)
    codigo = models.CharField(max_length=15, blank=False, unique=True)
    precio = models.DecimalField(max_digits=6,decimal_places=2)
    costo = models.DecimalField(max_digits=9,decimal_places=2)
    iva = models.DecimalField(max_digits=4,decimal_places=3, default=0.12)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=150, blank=False)
    ruc = models.BigIntegerField(validators=[RegexValidator(r'^[1-9]\d{9}$|^[1-9]\d{12}$')], unique=True)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    numero = models.BigIntegerField(max_length=150, blank=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.numero)

class Credito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    cupo = models.DecimalField(max_digits=6,decimal_places=2)
    saldo = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    activo = models.BooleanField(default=False)
    suspendido = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.cliente.nombre

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Consumo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    factura = models.ForeignKey(Factura, on_delete=models.SET_NULL, null=True)
    consumo = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    saldo = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    activo = models.BooleanField(default=False)
    suspendido = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.cliente.nombre)


def post_consumo(sender, instance, **kwargs):
    #instance.consumo.save()
    cliente = Cliente.objects.get(id=instance.cliente.id)
    factura = Factura.objects.get(id=instance.id)
    try:
        saldo_inicial = Consumo.objects.filter(cliente=cliente).order_by('-id')[0].saldo
    except:
        saldo_inicial = Credito.objects.get(cliente=cliente).cupo

    if saldo_inicial == "":
        saldo_inicial = Credito.objects.get(cliente=cliente).cupo
    saldo_consumo = saldo_inicial - instance.total
    print(factura)
    consumo = Consumo(factura=factura, cliente=cliente, consumo=instance.total, saldo=saldo_consumo)
    consumo.save()

post_save.connect(post_consumo, sender=Factura)
