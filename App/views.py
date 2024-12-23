from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail,EmailMultiAlternatives #libreria para email de django
from django.template.loader import render_to_string#enviar html en el email
from . models import *
from .forms import *
from django.utils.html import escape
from django.conf import settings
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives






#ventana de Inicio sin iniciar sesión
def index(request):
    productos = Producto.objects.all()
    usuarios = UsuarioGeneral.objects.all()[:5]
    categorias = CategoriaProducto.objects.all()
    
    return render(request, 'index.html', {
        'productos': productos,
        'usuarios': usuarios,
        'categorias': categorias,
    })




#funcion para Registro
def registro(request):
    if request.method == 'POST':
        form = UsuarioGeneralForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener los datos del formulario
            email = form.cleaned_data['email']
            rut = form.cleaned_data['rut_usuario']
            
            # Validar si el correo ya está registrado
            if UsuarioGeneral.objects.filter(email=email).exists():
                messages.error(request, "Este correo electrónico ya está registrado.")
                return render(request, 'registro.html', {'form': form})

            # Validar si el RUT ya está registrado
            if UsuarioGeneral.objects.filter(rut_usuario=rut).exists():
                messages.error(request, "Este RUT ya está registrado.")
                return render(request, 'registro.html', {'form': form})

            # Si pasa las validaciones, guardar el usuario
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])  # Establecer la contraseña de forma segura
            usuario.save()  # Guardar el usuario en la base de datos

            # Redirigir después de un registro exitoso
            messages.success(request, "¡Cuenta creada con éxito!")
            return redirect('index')
        else:
            # Si el formulario tiene errores, mostrar mensajes de error
            messages.error(request, "Rut o Correo electronico existente. Por favor, intenta nuevamente.")
    else:
        form = UsuarioGeneralForm()

    return render(request, 'registro.html', {'form': form})



#ventana de inicio logeado
@login_required
def home(request):
    # Obtener todos los productos creados por cualquier usuario
    productos = Producto.objects.all().order_by('-fecha_creacion')
   
    return render(request, 'home.html', {
        'productos': productos,
        'usuario': request.user  # Agregar la información del usuario para el sidebar
    })


#Iniciar Session
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Intentamos encontrar el usuario con el correo electrónico proporcionado
            try:
                # No es necesario usar UsuarioGeneral.objects.get, ya que authenticate ya lo hace
                user = authenticate(request, username=email, password=password)

                if user is not None:
                    # Si el usuario es autenticado, iniciamos sesión
                    login(request, user)
                    return redirect('home')  # Redirige al dashboard o página principal
                else:
                    # Si la autenticación falla (usuario o contraseña incorrectos)
                    messages.error(request, "Correo electrónico o contraseña incorrectos. Intenta nuevamente.")
            
            except UsuarioGeneral.DoesNotExist:
                # Si el usuario no existe (aunque authenticate maneja esto)
                messages.error(request, "El correo electrónico no está registrado.")
        
        else:
            # Si el formulario tiene errores (campos vacíos u otros errores)
            for field in form:
                if field.errors:
                    # Evitar mostrar mensaje de campos vacíos si ya hay errores en los campos específicos
                    break
            else:
                # Si no hay errores en los campos del formulario
                messages.error(request, "Correo o Contraseña incorectas!.")

    else:
        form = LoginForm()  # Si es una solicitud GET, simplemente mostramos el formulario vacío

    return render(request, 'login.html', {'form': form})




@login_required
def visita_perfil(request, usuario_id):
    usuario = UsuarioGeneral.objects.get(id=usuario_id)

    # Si el usuario envía el formulario de valoración desde el modal
    if request.method == 'POST' and 'valorar' in request.POST:
        form = ValoracionForm(request.POST)
        if form.is_valid():
            # Crear una nueva valoración vinculada al usuario autenticado
            valoracion = form.save(commit=False)
            valoracion.usuario = usuario  # Asocia la valoración al usuario que se está valorando
            valoracion.usuario_que_valora = request.user  # Asocia al usuario autenticado que realiza la valoración
            valoracion.save()
            return redirect('visita_perfil', usuario_id=usuario.id,)  # Redirige al mismo perfil tras guardar

    else:
        form = ValoracionForm()

    # Renderizar el perfil con el formulario de valoración
    return render(request, 'visita_Perfil.html', {
        'usuario': usuario,
        'form': form,
        'rango': range(5),
        'usuario_autenticado': request.user,#paser el usuario que visita al contexto para mostrar su imagen
    })



#editar Perfil
@login_required
def editar_perfil(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirige al login si el usuario no está autenticado

    usuario = request.user
    comunas = Comuna.objects.all()  # Obtiene todas las comunas

    if request.method == 'POST':
        form = UsuarioGeneralForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('editar_perfil')  # Redirige a la misma página tras guardar los cambios
    else:
        form = UsuarioGeneralForm(instance=usuario)

    return render(request, 'editar_perfil.html', {'usuario': usuario, 'comunas': comunas, 'form': form})



#Cerrar sesión
def custom_logout(request):
    logout(request)
    return redirect('index') #redirecciona al al pagina sin iniciar sesión




#crear Producto
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Asignar el usuario creador
            producto = form.save(commit=False)
            producto.usuario_creador = request.user
            producto.save()
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = ProductoForm()

    return render(request, 'crearProducto.html', {'form': form})




#detalle de un producto
@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)#id del producto para la url
    return render(request, 'detalle_producto.html', {'producto': producto})#objeto instanciado para la url


#ver mis productos
@login_required
def mis_publicaciones(request):
    """Vista para mostrar los productos creados por el usuario autenticado."""
    if request.user.is_authenticated:
        productos_usuario = Producto.objects.filter(usuario_creador=request.user).order_by('-fecha_creacion')
   
    else:
        productos_usuario = []

    return render(request, 'mis_productos.html', {
        'productos': productos_usuario,
    })



#Editar Producto
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('mis_publicaciones')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})



########eliminar Producto
@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST": 
        producto.delete()
        messages.success(request, f"El producto '{producto.nombre_producto}' ha sido eliminado.")
        return redirect('mis_publicaciones')
    return redirect('detalle_producto', producto_id=producto_id)  # Redirigir si no es POST


#############################################Postulaciones

# Postular donación
@login_required
def postular_donacion(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = DonacionForm(request.POST, request.FILES)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.producto = producto
            postulacion.donante = request.user
            postulacion.estado = 'pendiente'
            postulacion.save()

            # Cargar html del  correo a la vista
            propietario = producto.usuario_creador
            subject = f"Nueva postulación para tu producto '{producto.nombre_producto}'"
            html_content = render_to_string('notificacion_donacion.html', {
                'producto': producto,
                'postulacion': postulacion,
                'propietario': propietario,
                'donante': request.user,
            })

            email = EmailMultiAlternatives(
                subject=subject,
                body="Nueva postulación recibida",
                from_email='regala.recibe@gmail.com',
                to=[propietario.email],
            )
            email.attach_alternative(html_content, "text/html")

            # Adjuntar imagen del producto (reducida a la mitad)
            with open(producto.imagen.path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<producto_imagen>')
                email.attach(mime_image)

            # Adjuntar imagen de perfil del donante (reducida a la mitad)
            with open(request.user.imagen_perfil.path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<donante_imagen>')
                email.attach(mime_image)

            email.send()
            return redirect('mis_transacciones')
    else:
        form = DonacionForm()
    return render(request, 'postular_donacion.html', {'producto': producto, 'form': form})




#Postular a intercambio
@login_required
def postular_intercambio(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = IntercambioForm(request.POST, request.FILES)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.producto = producto
            postulacion.intercambiador = request.user
            postulacion.estado = 'pendiente'
            postulacion.save()

            # Cargar imágenes como contenido embebido
            propietario = producto.usuario_creador
            subject = f"Nueva propuesta de intercambio para tu producto '{producto.nombre_producto}'"
            html_content = render_to_string('notificacion_intercambio.html', {
                'producto': producto,
                'postulacion': postulacion,
                'propietario': propietario,
                'intercambiador': request.user,
            })

            email = EmailMultiAlternatives(
                subject=subject,
                body="Nueva propuesta de intercambio recibida",
                from_email='regala.recibe@gmail.com',
                to=[propietario.email],
            )
            email.attach_alternative(html_content, "text/html")

            # Adjuntar imagen del producto original (reducida a la mitad)
            with open(producto.imagen.path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<producto_imagen>')
                email.attach(mime_image)

            # Adjuntar imagen de perfil del intercambiador (reducida a la mitad)
            with open(request.user.imagen_perfil.path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<intercambiador_imagen>')
                email.attach(mime_image)

            # Adjuntar imagen del producto propuesto para intercambio
            with open(postulacion.foto.path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<producto_intercambio>')
                email.attach(mime_image)

            email.send()
            return redirect('mis_transacciones')
    else:
        form = IntercambioForm()
    return render(request, 'postular_intercambio.html', {'producto': producto, 'form': form})




#ver mis transsacciones
@login_required
def mis_transacciones(request):
    donaciones = Donacion.objects.filter(donante=request.user).order_by('-fecha_postulacion')
    intercambios = Intercambio.objects.filter(intercambiador=request.user).order_by('-fecha_postulacion')
    
    return render(request, 'mis_transacciones.html', {'donaciones': donaciones, 'intercambios': intercambios})



#Eliminar una postulaciones 
@login_required
def eliminar_postulacion(request, postulacion_id):
    try:
        # Intentar obtener la postulación realizada por el usuario actual
        postulacion = get_object_or_404(Donacion, id=postulacion_id, donante=request.user)
        
        # Confirmar que el método de solicitud es POST para evitar eliminaciones accidentales
        if request.method == 'POST':
            postulacion.delete()
            messages.success(request, "La postulación ha sido eliminada correctamente.")
            return redirect('mis_transacciones')
        else:
            # Si el método no es POST, renderizar una página de confirmación
            messages.warning(request, "Confirmación requerida para eliminar la postulación.")
            return render(request, 'confirmar_eliminacion.html', {'postulacion': postulacion})
    
    except Exception as e:
        # Manejar errores (por ejemplo, si no se encuentra la postulación)
        messages.error(request, f"Error al intentar eliminar la postulación: {e}")
        return redirect('mis_transacciones')






@login_required
def valorar_usuario(request, usuario_id):
    usuario = UsuarioGeneral.objects.get(id=usuario_id)

    if request.method == 'POST':
        form = ValoracionForm(request.POST)
        if form.is_valid():
            # Asociamos la valoración con el usuario autenticado y el usuario valorado
            valoracion = form.save(commit=False)
            valoracion.usuario = usuario
            valoracion.save()
            return redirect('perfil_usuario', usuario_id=usuario.id)  # Redirige al perfil del usuario valorado

    else:
        form = ValoracionForm()

    return render(request, 'valoracion_form.html', {'form': form, 'usuario': usuario})




#########Eliminar transacciones##############################
