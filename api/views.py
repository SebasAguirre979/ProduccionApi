from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Usuario, Cliente, Repuesto
from .serializers import *
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Sum, F
from datetime import datetime
from django.utils.timezone import make_aware


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UsuarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioVerificationView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        cedula = request.data.get('cedula')
        contrasena = request.data.get('contrasena')
        nombre = request.data.get('nombre')
        try:
            usuario = Usuario.objects.get(cedula=cedula)
        except Usuario.DoesNotExist:
            return Response({'mensaje': 'Usuario no encontrado'}, status=404)
        if not check_password(contrasena, usuario.contrasena):
            print(check_password(contrasena, usuario.contrasena))
            return Response({'mensaje': 'Contraseña incorrecta'}, status=400)
        serializer = self.get_serializer(usuario)
        print(check_password(contrasena, usuario.contrasena))
        return Response({'nombre': serializer.data['nombre'],'cedula': serializer.data['cedula']})
    
""" Ahora deberías tener un API REST en Django con las siguientes rutas:

GET /usuarios/: Obtiene una lista de todos los usuarios.
POST /usuarios/: Crea un nuevo usuario.
GET /usuarios/<id>/: Obtiene los detalles de un usuario específico.
PUT /usuarios/<id>/: Actualiza los detalles de un usuario específico.
DELETE /usuarios/<id>/: Elimina un usuario específico.
POST /usuarios/verificacion/: Verifica si un usuario existe en la base de datos según la cedula y la contraseña proporcionados.
Recuerda que este es solo un ejemplo básico y puede requerir ajustes según tus necesidades específicas, como agregar autenticación y permisos. """

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UsuarioCambioContrasenaView(APIView):
    def post(self, request, cedula):
        # Obtener los datos enviados en la solicitud POST
        contrasena_antigua = request.data.get('contrasena_antigua')
        contrasena_nueva = request.data.get('contrasena_nueva')

        if not contrasena_nueva:
            return Response({'error': 'La contraseña nueva no puede estar vacía'}, status=400)
        
        try:
            # Obtener el usuario por su cédula
            usuario = Usuario.objects.get(cedula=cedula)
        except Usuario.DoesNotExist:
            return Response({'error': 'El usuario no existe'}, status=400)

        # Verificar si la contraseña antigua coincide con la almacenada en la base de datos
        contrasena_coincide = check_password(contrasena_antigua, usuario.contrasena)
        if not contrasena_coincide:
            return Response({'error': 'La contraseña antigua es incorrecta'}, status=400)

        # Cambiar la contraseña y guardar el usuario
        usuario.contrasena = contrasena_nueva
        usuario.save()

        return Response({'mensaje': 'Contraseña cambiada exitosamente'})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ClienteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ClienteVehiculoVerificationView(APIView):

    def post(self, request, *args, **kwargs):
        cedula = request.data.get('cedula')
        placa = request.data.get('placa')

        response_data = {}

        cliente_exists = Cliente.objects.filter(cedula=cedula).exists()
        vehiculo_exists = Vehiculo.objects.filter(placa=placa).exists()

        if cliente_exists and vehiculo_exists:
            response_data['cedula'] = cedula
            response_data['placa'] = placa
        elif cliente_exists:
            response_data['cedula'] = cedula
            response_data['placa'] = 'Placa no existe'
        elif vehiculo_exists:
            response_data['cedula'] = 'Cedula no existe'
            response_data['placa'] = placa
        else:
            response_data['cedula'] = 'Cedula no existe'
            response_data['placa'] = 'Placa no existe'

        return Response(response_data)

class RepuestoListCreateView(generics.ListCreateAPIView):
    queryset = Repuesto.objects.all()
    serializer_class = RepuestoSerializer

class RepuestoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repuesto.objects.all()
    serializer_class = RepuestoSerializer

class RepuestoVerificationView(generics.GenericAPIView):
    serializer_class = RepuestoSerializer

    def post(self, request, *args, **kwargs):
        r_nombre_repuesto = request.data.get('r_nombre_repuesto')
        try:
            repuesto = Repuesto.objects.get(r_nombre_repuesto=r_nombre_repuesto)
        except Repuesto.DoesNotExist:
            return Response({'mensaje': 'Repuesto no encontrado'}, status=404)
        serializer = self.get_serializer(repuesto)
        return Response(serializer.data)

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

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class VehiculoListCreateView(generics.ListCreateAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class VehiculoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class VehiculoVerificationView(generics.GenericAPIView):
    serializer_class = VehiculoSerializer

    def post(self, request, *args, **kwargs):
        placa = request.data.get('placa')
        try:
            vehiculo = Vehiculo.objects.get(placa=placa)
        except Vehiculo.DoesNotExist:
            return Response({'mensaje': 'Vehiculo no encontrado'}, status=404)
        serializer = self.get_serializer(vehiculo)
        return Response(serializer.data)

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

#Me hace un post de un servicio con todo y repuestos incluidos
class ServicioRepuestosPost(APIView):
    serializer_class = ServicioSerializer
    def post(self, request, format=None):
        # Obtener los datos del servicio y los detalles de servicio del cuerpo de la solicitud
        servicio_data = request.data.get('servicio')
        detalles_servicio = request.data.get('detalles_servicio')

        # Verificar el stock de todos los repuestos antes de hacer cualquier cambio en la venta
        repuestos_sin_stock = []
        for detalle in detalles_servicio:
            repuesto_id = detalle.get('repuesto')
            cantidad = detalle.get('s_cantidad')

            repuesto = Repuesto.objects.get(pk=repuesto_id)
            if cantidad > repuesto.r_cantidad:
                repuestos_sin_stock.append(repuesto.r_nombre_repuesto)

        if repuestos_sin_stock:
            error_message = f"No hay suficiente stock para los siguientes repuestos: {', '.join(repuestos_sin_stock)}"
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear la venta
        servicio_serializer = ServicioSerializer(data=servicio_data)
        if servicio_serializer.is_valid():
            servicio = servicio_serializer.save()

            # Realizar los cambios en la venta solo si hay suficiente stock para todos los repuestos
            total_servicio = 0
            for detalle in detalles_servicio:
                repuesto_id = detalle.get('repuesto')
                cantidad = detalle.get('s_cantidad')

                repuesto = Repuesto.objects.get(pk=repuesto_id)

                # Calcular el subtotal del detalle de venta
                subtotal = cantidad * repuesto.r_valor_publico

                # Crear el detalle de venta asociado a la venta
                DetalleServicio.objects.create(servicio=servicio, repuesto=repuesto, s_cantidad=cantidad)

                # Restar el stock del repuesto
                repuesto.r_cantidad -= cantidad
                repuesto.save()

                # Sumar el subtotal al total de la venta
                total_servicio += subtotal

            # Actualizar el campo v_total de la venta
            servicio.s_total = total_servicio
            servicio.save()

            return Response({'message': 'Servicio creada exitosamente'}, status=201)
        else:
            return Response(servicio_serializer.errors, status=400)
        
    
    def get(self, request, format=None):
        servicios = Servicio.objects.all()
        serializer = self.serializer_class(servicios, many=True)
        return Response(serializer.data)

    
#Me muestra tanto el cliente y vehiculo completo de un servicio y repuestos
class ServicioRepuestosViewId(APIView):
    serializer_class = ServicioSerializer
    def get(self, request, servicio_id, format=None):
        try:
            servicio = Servicio.objects.get(id=servicio_id)
        except Servicio.DoesNotExist:
            return Response({'error': 'El servicio no existe'}, status=404)
        
        detalles_servicio = DetalleServicio.objects.filter(servicio=servicio)
        repuestos_data = []

        servicio_data = {
            'id': servicio.id,
            'cliente': {
                'cedula': servicio.cliente.cedula,
                'nombre': servicio.cliente.nombre,
                'celular': servicio.cliente.celular,
            },
            's_descripcion': servicio.s_descripcion,
            's_vehiculo': {
                'placa': servicio.s_vehiculo.placa,
                'tipo': servicio.s_vehiculo.tipo,
            },
            's_mano_obra': servicio.s_mano_obra,
            's_fecha_entrada': servicio.s_fecha_entrada,
            's_fecha_salida': servicio.s_fecha_salida,
            's_total': servicio.s_total,
            'detalles_servicio': repuestos_data,
        }
        
        for detalle in detalles_servicio:
            repuesto = detalle.repuesto
            repuesto_data = {
                'id': detalle.id,  # ID de DetalleServicio
                'r_nombre_repuesto': repuesto.r_nombre_repuesto,
                'ds_valor_publico': detalle.ds_valor_publico,
                's_cantidad': detalle.s_cantidad,
            }
            repuestos_data.append(repuesto_data)
        

        return Response(servicio_data, status=200)

#Agrega el detalle servicio y resta al inventario lo que se agrego ademas del total del servicio
class DetalleServicioPostAPIView(APIView):
    def post(self, request, servicio_id, format=None):
        try:
            servicio = Servicio.objects.get(pk=servicio_id)
        except Servicio.DoesNotExist:
            return Response({"detail": "El servicio no existe."}, status=404)

        repuesto_id = request.data.get('repuesto')
        s_cantidad = request.data.get('s_cantidad')

        if repuesto_id is None or s_cantidad is None:
            return Response({"detail": "Debes proporcionar el ID del repuesto y la cantidad."}, status=400)

        try:
            repuesto = Repuesto.objects.get(pk=repuesto_id)
        except Repuesto.DoesNotExist:
            return Response({"detail": "El repuesto no existe."}, status=404)

        s_cantidad = int(s_cantidad)

        if repuesto.r_cantidad < s_cantidad:
            return Response({"detail": "No hay suficiente inventario disponible para el repuesto."}, status=400)

        repuesto.r_cantidad -= s_cantidad
        repuesto.save()

        servicio.s_total += repuesto.r_valor_publico * s_cantidad
        servicio.save()

        detalle_servicio = DetalleServicio.objects.create(
            servicio=servicio,
            repuesto=repuesto,
            s_cantidad=s_cantidad
        )

        serializer = DetalleServicioSerializer(detalle_servicio)
        return Response(serializer.data, status=201)
    
#Elimina el detalle servicio y devuelve al inventario lo que se elimino del servicio
class DetalleServicioDeleteAPIView(APIView):
    def delete(self, request, detalle_servicio_id, format=None):
        try:
            detalle_servicio = DetalleServicio.objects.get(id=detalle_servicio_id)
        except DetalleServicio.DoesNotExist:
            return Response({'error': f'Detalle de servicio con ID {detalle_servicio_id} no encontrado.'}, status=400)
        
        servicio = detalle_servicio.servicio
        repuesto = detalle_servicio.repuesto
        repuesto.r_cantidad += detalle_servicio.s_cantidad
        servicio.s_total -= detalle_servicio.ds_valor_publico * detalle_servicio.s_cantidad
        repuesto.save()
        servicio.save()

        detalle_servicio.delete()

        return Response({'success': 'Detalle de servicio eliminado correctamente.'}, status=200)
    
#Actualiza el detalle servicio la cantidad del repuesto, sea que merme o aumente
class DetalleServicioUpdateAPIView(APIView):
    def put(self, request, detalle_servicio_id, format=None):
        try:
            detalle_servicio = DetalleServicio.objects.get(id=detalle_servicio_id)
        except DetalleServicio.DoesNotExist:
            return Response({'error': f'Detalle de servicio con ID {detalle_servicio_id} no encontrado.'}, status=400)
        
        nueva_cantidad = request.data.get('s_cantidad')

        if nueva_cantidad is None:
            return Response({'error': 'La nueva cantidad no se proporcionó correctamente.'}, status=400)

        repuesto = detalle_servicio.repuesto
        diferencia_cantidad = nueva_cantidad - detalle_servicio.s_cantidad

        if diferencia_cantidad > repuesto.r_cantidad:
            return Response({'error': 'No hay suficiente cantidad disponible en el inventario.'}, status=400)
        
        total_temporal = 0
        servicio = detalle_servicio.servicio
        total_temporal += nueva_cantidad * detalle_servicio.ds_valor_publico
        total_temporal -= detalle_servicio.s_cantidad * detalle_servicio.ds_valor_publico
        servicio.s_total += total_temporal
        servicio.save()
    
        detalle_servicio.s_cantidad = nueva_cantidad
        detalle_servicio.save()

        repuesto.r_cantidad -= diferencia_cantidad
        repuesto.save()

        return Response({'success': 'Detalle de servicio actualizado correctamente.'}, status=200)
    
class VentaRepuestosPost(APIView):
    def post(self, request, format=None):
        # Obtener los datos de la venta y los detalles de venta del cuerpo de la solicitud
        datos_venta = request.data.get('venta')
        detalles_venta = request.data.get('detalles_venta')

        # Verificar el stock de todos los repuestos antes de hacer cualquier cambio en la venta
        repuestos_sin_stock = []
        for detalle in detalles_venta:
            repuesto_id = detalle.get('repuesto')
            cantidad = detalle.get('v_cantidad')

            repuesto = Repuesto.objects.get(pk=repuesto_id)
            if cantidad > repuesto.r_cantidad:
                repuestos_sin_stock.append(repuesto.r_nombre_repuesto)

        if repuestos_sin_stock:
            error_message = f"No hay suficiente stock para los siguientes repuestos: {', '.join(repuestos_sin_stock)}"
            return Response({'error': error_message}, status=400)

        # Crear la venta
        venta_serializer = VentaSerializer(data=datos_venta)
        if venta_serializer.is_valid():
            venta = venta_serializer.save()

            # Realizar los cambios en la venta solo si hay suficiente stock para todos los repuestos
            total_venta = 0
            for detalle in detalles_venta:
                repuesto_id = detalle.get('repuesto')
                cantidad = detalle.get('v_cantidad')

                repuesto = Repuesto.objects.get(pk=repuesto_id)

                # Calcular el subtotal del detalle de venta
                subtotal = cantidad * repuesto.r_valor_publico

                # Crear el detalle de venta asociado a la venta
                DetalleVenta.objects.create(venta=venta, repuesto=repuesto, v_cantidad=cantidad)

                # Restar el stock del repuesto
                repuesto.r_cantidad -= cantidad
                repuesto.save()

                # Sumar el subtotal al total de la venta
                total_venta += subtotal

            # Actualizar el campo v_total de la venta
            venta.v_total = total_venta
            venta.save()

            # Obtener los detalles de venta asociados a la venta
            detalles_venta = DetalleVenta.objects.filter(venta=venta)

            # Serializar los detalles de venta con los datos de repuestos
            detalles_serializer = DetalleVentaSerializer(detalles_venta, many=True)

            # Obtener los datos de repuestos en cada detalle de venta
            repuestos_data = []
            for detalle in detalles_venta:
                repuesto_data = {
                    'r_nombre_repuesto': detalle.repuesto.r_nombre_repuesto,
                    'dv_valor_publico': detalle.dv_valor_publico,
                    'v_cantidad': detalle.v_cantidad
                }
                repuestos_data.append(repuesto_data)

            # Serializar la venta y agregar los datos de repuestos
            venta_serializer = VentaSerializer(venta)
            venta_data = venta_serializer.data
            venta_data['repuestos'] = repuestos_data

            return Response(venta_data, status=201)
        else:
            return Response(venta_serializer.errors, status=400)
        
class VentaRepuestosGetDelete(APIView):
    def get(self, request, venta_id, format=None):
        # Obtener la venta por su ID
        try:
            venta = Venta.objects.get(pk=venta_id)
        except Venta.DoesNotExist:
            return Response({'error': 'La venta especificada no existe'}, status=404)

        # Obtener los detalles de venta asociados a la venta
        detalles_venta = DetalleVenta.objects.filter(venta=venta)

        # Serializar los detalles de venta con los datos de repuestos
        detalles_serializer = DetalleVentaSerializer(detalles_venta, many=True)

        # Obtener los datos de repuestos en cada detalle de venta
        repuestos_data = []
        for detalle in detalles_venta:
            repuesto_data = {
                'r_nombre_repuesto': detalle.repuesto.r_nombre_repuesto,
                'dv_valor_publico': detalle.dv_valor_publico,
                'v_cantidad': detalle.v_cantidad
            }
            repuestos_data.append(repuesto_data)

        # Serializar la venta y agregar los datos de repuestos
        venta_serializer = VentaSerializer(venta)
        venta_data = venta_serializer.data
        venta_data['repuestos'] = repuestos_data

        return Response(venta_data)

    def delete(self, request, venta_id, format=None):
        # Obtener la venta por su ID
        try:
            venta = Venta.objects.get(pk=venta_id)
        except Venta.DoesNotExist:
            return Response({'error': 'La venta especificada no existe'}, status=404)

        # Obtener los detalles de venta asociados a la venta
        detalles_venta = DetalleVenta.objects.filter(venta=venta)

        # Restablecer los repuestos utilizados en el inventario
        for detalle in detalles_venta:
            repuesto = detalle.repuesto
            repuesto.r_cantidad += detalle.v_cantidad
            repuesto.save()

        # Eliminar la venta y los detalles de venta
        venta.delete()
        detalles_venta.delete()

        return Response({'message': 'La venta y sus detalles se han eliminado correctamente'}, status=200)

#Listar servicios por placa de un vehiculo
class ServicioDetalleView(APIView):   
    def get(self, request, vehiculo_id, format=None):
        servicios = Servicio.objects.filter(s_vehiculo_id=vehiculo_id)
        resultados = []

        for servicio in servicios:
            detalles = {
                "cliente": {
                    "cedula": servicio.cliente.cedula,
                    "nombre": servicio.cliente.nombre,
                    "celular": servicio.cliente.celular
                },
                "s_vehiculo": {
                    "placa": servicio.s_vehiculo.placa,
                    "tipo": servicio.s_vehiculo.tipo
                },
                "id": servicio.id,
                "s_descripcion": servicio.s_descripcion,
                "s_mano_obra": servicio.s_mano_obra,
                "s_fecha_entrada": servicio.s_fecha_entrada.isoformat(),
                "s_fecha_salida": servicio.s_fecha_salida.isoformat() if servicio.s_fecha_salida else None,
                "s_total": servicio.s_total,
                "estado": servicio.estado,
                "detalles_servicio": []
            }

            detalles_servicio = DetalleServicio.objects.filter(servicio=servicio)

            for detalle in detalles_servicio:
                detalles_repuesto = {
                    "r_nombre_repuesto": detalle.repuesto.r_nombre_repuesto,
                    "ds_valor_publico": detalle.ds_valor_publico,
                    "s_cantidad": detalle.s_cantidad
                }
                detalles["detalles_servicio"].append(detalles_repuesto)

            resultados.append(detalles)

        return Response(resultados, status=200)
    
class ReporteServicioView(APIView):

    def get(self, request, fecha_inicio, fecha_fin):
        fecha_inicio = make_aware(datetime.strptime(fecha_inicio, "%Y-%m-%d"))
        fecha_fin = make_aware(datetime.strptime(fecha_fin, "%Y-%m-%d"))

        # Filtrar los servicios en el intervalo de fechas dado
        servicios = Servicio.objects.filter(s_fecha_salida__range=[fecha_inicio, fecha_fin])

        # Calcular el total bruto sumando los totales de todos los servicios
        total_bruto = servicios.aggregate(Sum('s_total'))['s_total__sum'] or 0

        # Calcular las ganancias
        detalle_servicios = DetalleServicio.objects.filter(servicio__in=servicios)
        costo_repuestos = detalle_servicios.annotate(total_costo=F('s_cantidad') * F('ds_valor_proveedor')).aggregate(Sum('total_costo'))['total_costo__sum'] or 0
        ganancias = total_bruto - costo_repuestos

        # Generar el resumen de los servicios
        resumen_servicios = []
        for servicio in servicios:
            detalles = DetalleServicio.objects.filter(servicio=servicio)
            detalle_data = []

            for detalle in detalles:
                detalle_data.append({
                    'r_nombre_repuesto': detalle.repuesto.r_nombre_repuesto,
                    's_cantidad': detalle.s_cantidad,
                    'ds_valor_proveedor': detalle.ds_valor_proveedor,
                    'ds_valor_publico': detalle.ds_valor_publico
                })

            resumen_servicios.append({
                'id': servicio.id,
                'cliente': servicio.cliente.cedula,
                'vehiculo':servicio.s_vehiculo.placa,
                'descripcion': servicio.s_descripcion,
                's_fecha_salida': servicio.s_fecha_salida,
                's_mano_obra': servicio.s_mano_obra,
                's_total': servicio.s_total,
                'detalle_servicio': detalle_data
            })

        # Retorna el resultado
        return Response({
            'total_bruto': total_bruto,
            'ganancias': ganancias,
            'resumen_servicios': resumen_servicios
        })

class ReporteVentaView(APIView):

    def get(self, request, fecha_inicio, fecha_fin):
        fecha_inicio = make_aware(datetime.strptime(fecha_inicio, "%Y-%m-%d"))
        fecha_fin = make_aware(datetime.strptime(fecha_fin, "%Y-%m-%d"))

        # Filtrar las ventas en el intervalo de fechas dado
        ventas = Venta.objects.filter(v_fecha__range=[fecha_inicio, fecha_fin])

        # Calcular el total bruto sumando los totales de todas las ventas
        total_bruto = ventas.aggregate(Sum('v_total'))['v_total__sum'] or 0

        # Calcular las ganancias
        detalle_ventas = DetalleVenta.objects.filter(venta__in=ventas)
        costo_repuestos = detalle_ventas.annotate(total_costo=F('v_cantidad') * F('dv_valor_proveedor')).aggregate(Sum('total_costo'))['total_costo__sum'] or 0
        ganancias = total_bruto - costo_repuestos

        # Generar el resumen de las ventas
        resumen_ventas = []
        for venta in ventas:
            detalles = DetalleVenta.objects.filter(venta=venta)
            detalle_data = []

            for detalle in detalles:
                detalle_data.append({
                    'r_nombre_repuesto': detalle.repuesto.r_nombre_repuesto,
                    'v_cantidad': detalle.v_cantidad,
                    'dv_valor_proveedor': detalle.dv_valor_proveedor,
                    'dv_valor_publico': detalle.dv_valor_publico
                })

            resumen_ventas.append({
                'id': venta.id,
                'cliente': venta.cliente.cedula,
                'v_fecha': venta.v_fecha,
                'v_total': venta.v_total,
                'detalle_venta': detalle_data
            })

        # Retorna el resultado
        return Response({
            'total_bruto': total_bruto,
            'ganancias': ganancias,
            'resumen_ventas': resumen_ventas
        })