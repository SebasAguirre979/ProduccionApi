from django.contrib import admin
from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioRetrieveUpdateDestroyView.as_view(), name='usuario-retrieve-update-destroy'),
    path('usuarios/verificacion/', UsuarioVerificationView.as_view(), name='usuario-verification'),
    path('usuarios/cambiocontrasena/<int:cedula>/', UsuarioCambioContrasenaView.as_view(), name='cambio-contrasena'),
    path('clientes/', ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('clientes/<int:pk>/', ClienteRetrieveUpdateDestroyView.as_view(), name='cliente-retrieve-update-destroy'),
    path('clientes/verificacion/', ClienteVerificationView.as_view(), name='cliente-verification'),
    path('repuestos/', RepuestoListCreateView.as_view(), name='repuesto-list-create'),
    path('repuestos/<int:pk>/', RepuestoRetrieveUpdateDestroyView.as_view(), name='repuesto-retrieve-update-destroy'),
    path('ventas/', VentaListCreateView.as_view(), name='venta-list-create'),
    path('ventas/<int:pk>/', VentaRetrieveUpdateDestroyView.as_view(), name='venta-retrieve-update-destroy'),
    path('detalleventas/', DetalleVentaListCreateView.as_view(), name='detalleventa-list-create'),
    path('detalleventas/<int:pk>/', DetalleVentaRetrieveUpdateDestroyView.as_view(), name='detalleventa-retrieve-update-destroy'),
    path('vehiculos/', VehiculoListCreateView.as_view(), name='vehiculo-list-create'),
    path('vehiculos/<str:pk>/', VehiculoRetrieveUpdateDestroyView.as_view(), name='vehiculo-retrieve-update-destroy'),
    path('vehiculos-verificacion/', VehiculoVerificationView.as_view(), name='vehiculo-verification'),
    path('servicios/', ServicioListCreateView.as_view(), name='servicio-list-create'),
    path('servicios/<int:pk>/', ServicioRetrieveUpdateDestroyView.as_view(), name='servicio-retrieve-update-destroy'),
    path('detalleservicios/', DetalleServicioListCreateView.as_view(), name='detalleservicio-list-create'),
    path('detalleservicios/<int:pk>/', DetalleServicioRetrieveUpdateDestroyView.as_view(), name='detalleservicio-retrieve-update-destroy'),
    path('valoraciones/', ValoracionListCreateView.as_view(), name='valoracion-list-create'),
    path('valoraciones/<int:pk>/', ValoracionRetrieveUpdateDestroyView.as_view(), name='valoracion-retrieve-update-destroy'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    #para pruebas de servicio completo
    path('serviciosconrepuestos/', ServicioRepuestosPost.as_view(), name='add-servicio-con-todos-sus-componentes'),
    path('servicioclientevehiculo/<int:servicio_id>/', ServicioRepuestosViewId.as_view(), name='servicio-cliente-vehiculo-get-id-servicio'),
    path('createrepuesto/<int:servicio_id>/', DetalleServicioPostAPIView.as_view(), name='crea-repuesto-a-servicio-por-id-de-servicio'),
    path('deleterepuesto/<int:detalle_servicio_id>/', DetalleServicioDeleteAPIView.as_view(), name='elimina-repuesto-por-detalleservicio-id'),
    path('updaterepuesto/<int:detalle_servicio_id>/', DetalleServicioUpdateAPIView.as_view(), name='actualiza-repuesto-por-detalleservicio-id'),
    path('ventarepuestos/', VentaRepuestosPost.as_view(), name='crea-venta-repuestos'),
    path('ventarepuestos/<int:venta_id>/', VentaRepuestosGetDelete.as_view(), name='get-venta-por-id-y-delete'),
    path('serviciosplaca/<str:vehiculo_id>/', ServicioDetalleView.as_view(), name='get-servicios-vehiculo-por-placa'),
    path('reporte-servicio/<str:fecha_inicio>/<str:fecha_fin>/', ReporteServicioView.as_view()),
    path('reporte-venta/<str:fecha_inicio>/<str:fecha_fin>/', ReporteVentaView.as_view()),
    path('verificacion-vehiculo-cliente/', ClienteVehiculoVerificationView.as_view()),
]

