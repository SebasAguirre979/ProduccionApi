from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone

# Create your models here.
class Usuario(models.Model):
    cedula = models.BigIntegerField(primary_key=True)
    contrasena = models.CharField(max_length=128, blank=False)
    nombre = models.CharField(max_length=255, blank=False)
    celular = models.BigIntegerField()
    rol = models.CharField(max_length=10, blank=False)
    def save(self, *args, **kwargs):
        self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)
    class Meta:
        db_table = "usuario"

class Cliente(models.Model):
    cedula = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False)
    celular = models.BigIntegerField()
    class Meta:
        db_table = "cliente"

class Repuesto(models.Model):
    r_nombre_repuesto = models.CharField(max_length=30, unique=True)
    r_cantidad = models.IntegerField(blank=False)
    r_valor_proveedor = models.FloatField(blank=False)
    r_valor_publico = models.FloatField(blank=False)
    class Meta:
        db_table = "repuesto"

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    v_fecha = models.DateTimeField(default=timezone.now, editable=False)
    v_total = models.FloatField(default=0, editable=False)
    class Meta:
        db_table = "venta"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo venta
            self.v_fecha = timezone.now()  # Guardar la fecha de entrada
        super().save(*args, **kwargs)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    v_cantidad = models.IntegerField(blank=False)
    dv_valor_proveedor = models.FloatField(blank=False, default=0.0)
    dv_valor_publico = models.FloatField(blank=False, default=0.0)
    class Meta:
        db_table = "detalleVenta"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo detalleventa
            self.dv_valor_proveedor = self.repuesto.r_valor_proveedor
            self.dv_valor_publico = self.repuesto.r_valor_publico  # Guardar la el valor actual
        super().save(*args, **kwargs)

class Vehiculo(models.Model):
    placa = models.CharField(primary_key=True, max_length=6)
    tipo = models.CharField(max_length=20)
    class Meta:
        db_table = "vehiculo"

class Servicio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    s_descripcion = models.CharField(max_length=100)
    s_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    s_mano_obra = models.FloatField(blank=True, null=True, default=0)
    s_fecha_entrada = models.DateTimeField(default=timezone.now, editable=False)
    s_fecha_salida = models.DateTimeField(blank=True, null=True, editable=False)
    s_total = models.FloatField(default=0, editable=False)
    estado = models.BooleanField(default=True)
    class Meta:
        db_table = "servicio"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo servicio
            self.s_fecha_entrada = timezone.now()  # Guardar la fecha de entrada
        elif not self.estado:  # Si el estado cambió a False
            self.s_fecha_salida = timezone.now()  # Guardar la fecha de salida
            self.s_total += self.s_mano_obra
        super().save(*args, **kwargs)

class DetalleServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    s_cantidad = models.IntegerField(blank=False)
    ds_valor_proveedor = models.FloatField(blank=False, default=0.0)
    ds_valor_publico = models.FloatField(blank=False, default=0.0)
    class Meta:
        db_table = "detalleServicio"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo detalleservicio
            self.ds_valor_proveedor = self.repuesto.r_valor_proveedor
            self.ds_valor_publico = self.repuesto.r_valor_publico  # Guardar la el valor actual
        super().save(*args, **kwargs)

class Valoracion(models.Model):
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE)
    calificacion = models.IntegerField(blank=False)
    opinion = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(default=timezone.now, editable=False)
    class Meta:
        db_table = "valoracion"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva valoracion
            self.fecha = timezone.now()  # Guardar la fecha de entrada
        super().save(*args, **kwargs)