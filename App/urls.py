from django.urls import path
from . views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views






urlpatterns = [
    path('', index, name='index'),  # Ruta  index
    path('login/', login_view, name='login'), 
    path('logout/', custom_logout, name='logout'),
    path('registrarse/', registro, name='registro'),
    path('home/',home, name='home'),#pagina principal logeado
    #usuarios 
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('perfil/<int:usuario_id>/',visita_perfil, name='visita_perfil'),#visitar perfil de otro Usuario
    #productos
    path('crearProducto/',crear_producto,name='crearProducto'),#publicar producto
    path('producto/<int:producto_id>/',detalle_producto,name='detalle_producto'),
    path('mis-publicaciones/', mis_publicaciones, name='mis_publicaciones'),
    path('editar_producto/<int:producto_id>', editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/',eliminar_producto, name='eliminar_producto'),
    #postulaciones
    path('producto/<int:producto_id>/postular/donacion/', postular_donacion, name='postular_donacion'),
    path('producto/<int:producto_id>/postular/intercambio/',postular_intercambio, name='postular_intercambio'),
    path('historial_transacciones/', mis_transacciones, name='mis_transacciones'),
    #eliminar mis postulaciones realizadas
]
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)