from django import forms
from django.contrib.auth import authenticate
from .models import *
from django.core.exceptions import ValidationError

from django import template




#Django aplica un algoritmo de hashing seguro (como PBKDF2) y guarda el valor cifrado en la base de datos
# Formulario para crear o actualizar Usuario General con contraseña


class UsuarioGeneralForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Crea una contraseña'})
    )
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirma tu contraseña'})
    )
    imagen_perfil = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        empty_label="Selecciona tu comuna",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),  # Inicialmente no hay ciudades
        empty_label="Selecciona tu ciudad",
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False  # Solo si es necesario
    )

    class Meta:
        model = UsuarioGeneral
        fields = [
            'email', 'rut_usuario', 'nombre', 'apellido',
            'telefono', 'fecha_nacimiento', 'comuna', 'ciudad', 'imagen_perfil'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Ingresa tu correo electrónico'}),
            'rut_usuario': forms.TextInput(attrs={'placeholder': 'Ingresa tu RUT'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingresa tu nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingresa tu apellido'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingresa tu número de teléfono'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si se está recibiendo datos, filtrar las ciudades según la comuna seleccionada
        if 'comuna' in self.data:
            try:
                comuna_id = int(self.data.get('comuna'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(comuna_id=comuna_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Si es un usuario existente, cargar la ciudad según la comuna seleccionada
            self.fields['ciudad'].queryset = self.instance.comuna.ciudades.all()

        # Filtrar las comunas en función de la ciudad seleccionada (esto lo hacemos aquí)
        if 'ciudad' in self.data:
            try:
                ciudad_id = int(self.data.get('ciudad'))
                self.fields['comuna'].queryset = Comuna.objects.filter(ciudad_id=ciudad_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Si el usuario ya tiene una ciudad asociada, podemos cargar las comunas correspondientes
            self.fields['comuna'].queryset = self.instance.ciudad.comunas.all()




# 

###Formulario para logearse

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'Ingresa tu correo electrónico'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Validar que ambos campos estén completos
        if not email or not password:
            raise ValidationError("Por favor, ingresa tanto tu correo electrónico como tu contraseña.")

        if email and password:
            # Intentamos encontrar al usuario con el correo electrónico proporcionado
            try:
                user = UsuarioGeneral.objects.get(email=email)
                # Usamos el email como 'username' para autenticar
                authenticated_user = authenticate(username=user.email, password=password)

                if authenticated_user is None:
                    raise ValidationError("Correo electrónico o contraseña incorrectos.")
            except UsuarioGeneral.DoesNotExist:
                raise ValidationError("El correo electrónico no está registrado.")

        return cleaned_data

# Formulario para Valoracion
class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = '__all__'

# Formulario para Ciudad
class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = '__all__'

# Formulario para Comuna
class ComunaForm(forms.ModelForm):
    class Meta:
        model = Comuna
        fields = '__all__'

# Formulario para CategoriaProducto
class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = '__all__'

#formulario Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'descripcion', 'estado', 'categoria', 'tipo_transaccion','imagen']  # Incluye tipo_transaccion

    tipo_transaccion = forms.ModelChoiceField(queryset=TipoTransaccion.objects.all(), empty_label="Seleccione un tipo de transacción")

class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = ['comentario']  # Campos que se van a mostrar en el formulario, se elimina Producto
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comentario'].required = False  # Comentario no es obligatorio
        #self.fields['producto'].required = True  # Producto obligatorio

    def save(self, commit=True):
        # Si no hay comentario, poner el valor por defecto
        if not self.cleaned_data['comentario']:
            self.cleaned_data['comentario'] = 'Ningún comentario'
        return super().save(commit=commit)



class IntercambioForm(forms.ModelForm):
    class Meta:
        model = Intercambio
        fields = ['nombre_nuevo_producto', 'descripcion', 'foto','comentario']  # Excluye 'producto'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nombre_nuevo_producto'].required = True
        self.fields['descripcion'].required = True
        self.fields['foto'].required = False
        self.fields['comentario'].required = False





class UsuarioGeneralForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Crea una contraseña'})
    )
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirma tu contraseña'})
    )
    imagen_perfil = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        empty_label="Selecciona tu comuna",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        empty_label="Selecciona tu ciudad",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = UsuarioGeneral
        fields = [
            'email', 'rut_usuario', 'nombre', 'apellido',
            'telefono', 'fecha_nacimiento', 'comuna', 'ciudad', 'imagen_perfil'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Ingresa tu correo electrónico'}),
            'rut_usuario': forms.TextInput(attrs={'placeholder': 'Ingresa tu RUT'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingresa tu nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingresa tu apellido'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingresa tu número de teléfono'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        
        return cleaned_data        
    


#Formulario para la Valoración
class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['puntaje', 'resena']
        widgets = {
            'puntaje': forms.Select(choices=[(i, i) for i in range(1, 6)]),  # Escoge un puntaje entre 1 y 5
            'resena': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu reseña...'})
        }