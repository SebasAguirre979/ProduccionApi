from rest_framework import generics
from rest_framework.response import Response
from .models import Usuario, Cliente, Repuesto
from .serializers import *
from django.contrib.auth.hashers import check_password

class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioVerificationView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        correo = request.data.get('correo')
        contrasena = request.data.get('contrasena')
        nombre = request.data.get('nombre')
        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return Response({'mensaje': 'Usuario no encontrado'}, status=404)
        if not check_password(contrasena, usuario.contrasena):
            return Response({'mensaje': 'Contraseña incorrecta'}, status=400)
        serializer = self.get_serializer(usuario)
        return Response({'nombre': serializer.data['nombre']})
    
""" Ahora deberías tener un API REST en Django con las siguientes rutas:

GET /usuarios/: Obtiene una lista de todos los usuarios.
POST /usuarios/: Crea un nuevo usuario.
GET /usuarios/<id>/: Obtiene los detalles de un usuario específico.
PUT /usuarios/<id>/: Actualiza los detalles de un usuario específico.
DELETE /usuarios/<id>/: Elimina un usuario específico.
POST /usuarios/verificacion/: Verifica si un usuario existe en la base de datos según el correo y la contraseña proporcionados.
Recuerda que este es solo un ejemplo básico y puede requerir ajustes según tus necesidades específicas, como agregar autenticación y permisos. """

class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteVerificationView(generics.GenericAPIView):
    serializer_class = ClienteSerializer

    def post(self, request, *args, **kwargs):
        cedula = request.data.get('cedula')
        try:
            cliente = Cliente.objects.get(cedula=cedula)
        except Cliente.DoesNotExist:
            return Response({'mensaje': 'Cliente no encontrado'}, status=404)
        serializer = self.get_serializer(cliente)
        return Response(serializer.data)

class RepuestoListCreateView(generics.ListCreateAPIView):
    queryset = Repuesto.objects.all()
    serializer_class = RepuestoSerializer

class RepuestoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repuesto.objects.all()
    serializer_class = RepuestoSerializer

class VentaListCreateView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class VentaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class DetalleVentaListCreateView(generics.ListCreateAPIView):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class DetalleVentaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class VehiculoListCreateView(generics.ListCreateAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class VehiculoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class ServicioListCreateView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class ServicioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class DetalleServicioListCreateView(generics.ListCreateAPIView):
    queryset = DetalleServicio.objects.all()
    serializer_class = DetalleServicioSerializer

class DetalleServicioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetalleServicio.objects.all()
    serializer_class = DetalleServicioSerializer

class ValoracionListCreateView(generics.ListCreateAPIView):
    queryset = Valoracion.objects.all()
    serializer_class = ValoracionSerializer

class ValoracionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Valoracion.objects.all()
    serializer_class = ValoracionSerializer