#archivo de todas las configuraciones del proyecto
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u)!3^!02p9wq$5b2prpo4fyb#%n%9d0n7ozn80qe3sm^i6&4uw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.ngrok-free.app', 'localhost', '127.0.0.1']#permitir visualizar por ngrok


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #sesion 
    #'App.middleware.SessionExpirationMiddleware', 
]

ROOT_URLCONF = 'regala_y_recibe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'regala_y_recibe.wsgi.application'



DATABASES = { 
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#almacenar la media de los moelos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#  sesión caduque cuando se cierra el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Configura la duración de la sesión (en segundos)
SESSION_COOKIE_AGE = 3600  # 1 hora:3600seg




# Configuración de correo electrónico en Django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Usamos Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'regala.recibe@gmail.com'  
EMAIL_HOST_PASSWORD ='xyzetmvhncroozkm'  


#auth para este modelo
AUTH_USER_MODEL = 'App.UsuarioGeneral' 



CSRF_COOKIE_SECURE = True 

#servidor de confio de los cfrs en el teléfono,varia cada vez quese ejecuta ngrok ,pero cambia cada vez 
CSRF_TRUSTED_ORIGINS = [
    'https://98f9-186-174-25-229.ngrok-free.app',
]


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ADMIN_SITE_HEADER = 'Panel de Administración'
ADMIN_SITE_TITLE = 'Panel de Administración Regala y Recibe'