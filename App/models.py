from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg

# Modelo de UsuarioGeneral
class UsuarioGeneral(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  # Haz que 'username' sea opcional.
    email = models.EmailField('Correo electrónico', unique=True)
    rut_usuario = models.CharField(max_length=11, unique=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    comuna = models.ForeignKey('Comuna', on_delete=models.CASCADE, blank=True, null=True)
    imagen_perfil = models.ImageField(upload_to='perfil_images/', null=True, blank=True)

    # Añadir un related_name para evitar conflictos
    groups = models.ManyToManyField('auth.Group', related_name='usuario_general_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuario_general_permissions_set', blank=True)

    USERNAME_FIELD = 'email'  # Define que el email será el identificador principal
    REQUIRED_FIELDS = ['username', 'nombre', 'apellido', 'telefono','imagen_perfil']  # Los campos requeridos para la creación del superusuario.

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"
    
    #calcular el promedio de valoraciones
    def obtener_promedio_valoraciones(self):
        promedio = self.valoraciones.aggregate(Avg('puntaje'))['puntaje__avg']
        return round(promedio, 2) if promedio is not None else 0.0

# Modelo de Valoración
class Valoracion(models.Model):
    resena = models.TextField(blank=True, null=True)
    puntaje = models.IntegerField()
    fecha_valoracion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('UsuarioGeneral', on_delete=models.CASCADE, related_name='valoraciones')
    
    # Definir un valor por defecto con el ID de un usuario específico
    usuario_que_valora = models.ForeignKey(
        'UsuarioGeneral', 
        on_delete=models.CASCADE, 
        related_name='valoraciones_hechas',
        default=1  # Este es el ID del usuario que se usará como valor por defecto
    )

    def __str__(self):
        return f"Valoración {self.id}: {self.puntaje}"
    


# Modelo de Ciudad
class Ciudad(models.Model):
    nombre_ciudad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_ciudad


# Modelo de Comuna
class Comuna(models.Model):
    nombre_comuna = models.CharField(max_length=150)
    ciudad = models.ForeignKey('Ciudad', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_comuna


# Modelo de Categoría de Producto
class CategoriaProducto(models.Model):
    nombre_categoria = models.CharField(max_length=250)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_categoria


# Modelo de Tipo de Transacción
class TipoTransaccion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# Modelo de Producto
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=250)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL, null=True, blank=True)  # Cambié a SET_NULL por si se elimina la categoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creador = models.ForeignKey(UsuarioGeneral, on_delete=models.CASCADE, related_name='productos')  # Relación con Usuario
    tipo_transaccion = models.ForeignKey(TipoTransaccion, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con TipoTransaccion
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_producto} {self.imagen}"

    

#modelo para donacion 
class Donacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relacionado con el producto donado
    comentario = models.TextField(default='Ningún comentario')  # Comentario sobre la donación
    donante = models.ForeignKey(UsuarioGeneral, on_delete=models.CASCADE)  # Usuario que hace la donación
    fecha_postulacion = models.DateTimeField(auto_now_add=True)  # Fecha en que se realiza la donación
    estado = models.CharField(max_length=10, default='pendiente')  # Estado de la donación (pendiente por defecto)

    def __str__(self):
        return f"Donación de {self.producto.nombre_producto} por {self.donante.username}"

    def cambiar_estado(self, nuevo_estado):
        """
        Cambiar el estado de la donación de manera controlada.
        """
        self.estado = nuevo_estado
        self.save()

   

#modelo para intercambio
class Intercambio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relacionado con el producto original
    comentario = models.TextField(default='Ningún comentario')  # Comentario sobre el intercambio
    nombre_nuevo_producto = models.CharField(max_length=200)  # Nombre del producto intercambiado
    descripcion = models.TextField()  # Descripción del producto intercambiado
    foto = models.ImageField(upload_to='fotos_intercambio/', null=True, blank=True)  # Foto del producto intercambiado
    intercambiador = models.ForeignKey(UsuarioGeneral, on_delete=models.CASCADE, null=True)  # Usuario que realiza el intercambio
    fecha_postulacion = models.DateTimeField(auto_now_add=True)  # Fecha en que se realiza la postulación
    estado = models.CharField(max_length=50, default='pendiente')  # Estado del intercambio (pendiente por defecto)

    def __str__(self):
        return f"Intercambio de {self.producto.nombre_producto} por {self.nombre_nuevo_producto}"

    def cambiar_estado(self, nuevo_estado):
        """
        Cambiar el estado del intercambio de manera controlada.
        """
        self.estado = nuevo_estado
        self.save()
        
        #Para renderizarlo en el template
    def get_tipo_transaccion(self):
        return "Intercambio"    


