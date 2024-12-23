from django.contrib import admin
from django.urls import path,include 
from django.conf import settings
from django.conf.urls.static import static

#urls del Proyecto, incluye las urls de cada App 'Modulo'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),
]

# Configuración para servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)