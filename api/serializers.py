from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['cedula', 'contrasena', 'nombre', 'rol']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class RepuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuesto
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class DetalleServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleServicio
        fields = '__all__'

class ValoracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valoracion
        fields = '__all__'