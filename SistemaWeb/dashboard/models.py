from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.username.capitalize()
    

class Vendedor(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=200)
    celular = models.CharField(max_length=9)

    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    atencion = models.CharField(max_length=50)
    cliente = models.CharField(max_length=50)
    ruc_dni = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=200)
    obs= models.CharField(max_length=200,blank=True)
    
    def __str__(self):
        return self.cliente

class Direccion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200,blank=True)
    def __str__(self):
        return self.direccion

class Moneda(models.Model):
    SOLES= 'soles'
    DOLARES= 'dolares'
    ROL_CHOICES=[
        (SOLES,'Soles'),
        (DOLARES,'Dolares')
    ]
    tipo = models.CharField(max_length=20,choices=ROL_CHOICES)
    def __str__(self):
        return self.tipo

class Pago(models.Model):
    condicion = models.CharField(max_length=20)
    def __str__(self):
        return self.condicion
class Bu(models.Model):
    bu=models.CharField(max_length=200)
    def __str__(self):
        return self.bu
class Proforma(models.Model):
    fecha = models.DateField(auto_now=True)
    bu = models.ForeignKey(Bu, on_delete=models.CASCADE)
    condicion_pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    validez = models.CharField(max_length=20)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    correo = models.CharField(max_length=200, blank=True)
    celular = models.CharField(max_length=9, blank=True)
    def __str__(self):
        year = self.fecha.year % 100
        month = self.fecha.month

        return f"Proforma {self.id}-OPDM{year}.{month}"

#Signals 

@receiver(post_save, sender=Proforma)
def update_vendedor_info(sender, instance, created, **kwargs):
    if created and instance.vendedor:
        if not instance.correo:
            instance.correo = instance.vendedor.correo
        if not instance.celular:
            instance.celular = instance.vendedor.celular
        instance.save()

    
'''
@receiver(pre_save, sender=Proforma)
def update_vendedor_info(sender, instance, **kwargs):
    if instance.vendedor:
        vendedor_actual = instance.vendedor
        vendedor_antiguo = Proforma.objects.filter(pk=instance.pk).first()

        if vendedor_actual != vendedor_antiguo.vendedor:
            instance.correo = vendedor_actual.correo
            instance.celular = vendedor_actual.celular
'''
@receiver(pre_save, sender=Proforma)
def update_vendedor_info(sender, instance, **kwargs):
    if instance.vendedor:
        vendedor_actual = instance.vendedor
        try:
            # Obtener la instancia existente de Proforma desde la base de datos
            vendedor_antiguo = Proforma.objects.get(pk=instance.pk)
            
            if vendedor_actual != vendedor_antiguo.vendedor:
                instance.correo = vendedor_actual.correo
                instance.celular = vendedor_actual.celular
        except Proforma.DoesNotExist:
            # La instancia de Proforma es nueva, no es necesario hacer nada
            pass
