from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class Usuario(models.Model):
    cedula = models.BigIntegerField(primary_key=True)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    nombre = models.CharField(max_length=255)
    celular = models.BigIntegerField()
    rol = models.CharField(max_length=10)
    def save(self, *args, **kwargs):
        self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)
    class Meta:
        db_table = "usuario"

class Cliente(models.Model):
    cedula = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    celular = models.BigIntegerField()
    class Meta:
        db_table = "cliente"

class Repuesto(models.Model):
    r_nombre_repuesto = models.CharField(max_length=30, unique=True)
    r_cantidad = models.IntegerField()
    r_valor_proveedor = models.FloatField()
    r_valor_publico = models.FloatField()
    class Meta:
        db_table = "repuesto"

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    v_descripcion = models.CharField(max_length=100)
    v_fecha = models.DateTimeField()
    class Meta:
        db_table = "venta"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    v_cantidad = models.IntegerField()
    class Meta:
        db_table = "detalleVenta"

class Vehiculo(models.Model):
    placa = models.CharField(primary_key=True, max_length=6)
    tipo = models.CharField(max_length=20)
    class Meta:
        db_table = "vehiculo"

class Servicio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    s_descripcion = models.CharField(max_length=100)
    s_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    s_mano_obra = models.FloatField()
    s_fecha_entrada = models.DateTimeField()
    s_fecha_salida = models.DateTimeField()
    class Meta:
        db_table = "servicio"

class DetalleServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    s_cantidad = models.IntegerField()
    class Meta:
        db_table = "detalleServicio"

class Valoracion(models.Model):
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE)
    calificacion = models.IntegerField()
    opinion = models.CharField(max_length=255)
    class Meta:
        db_table = "valoracion"