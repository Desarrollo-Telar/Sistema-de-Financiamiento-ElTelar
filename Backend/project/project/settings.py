
from pathlib import Path
import os.path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f(l@4iukkrz%^l92ant-7xc4s%k1l%u_5a^#e3(f%3wi*3lutw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users',
    'apps.customers',
    'apps.roles',
    'crispy_forms',
    'apps.codes',
    'apps.pictures',
    'apps.addresses',
    'apps.FinancialInformation',
    'apps.InvestmentPlan',
    'rest_framework',
    'coreapi', 
    'apps.documents',
    'apps.financings',
    'django_celery_beat',
    #'bootstrap5',
    #'django_inlinecss',
    #'otp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # MIDDLEWARE 
    #'project.middleware.AutoLogoutMiddleware',
    #'project.middleware.RestrictedAccessByTimeMiddleware',
    # WhiteNoise 
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Modo de mantenimiento
MAINTENANCE_MODE = True  # Cambia a False para desactivar el modo de mantenimiento

# Configura el tiempo de expiración de la sesión a 30 minutos
SESSION_COOKIE_AGE = 1800  # 30 minutos en segundos

# Define que la sesión se cierre cuando el navegador se cierre
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Opcional: Si deseas que se borre la sesión de la base de datos al expirar
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



# Definir las horas de acceso permitido
ALLOWED_ACCESS_START_HOUR = 1   # Hora de inicio permitida (01:00 AM)

ALLOWED_ACCESS_END_HOUR = 23    # Hora de fin permitida (11:00 PM)

EXEMPT_PATHS = [
    '/admin/',
   
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
ROOT_URLCONF = 'project.urls'

# Configuración de autenticación
AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
"""
import project.database as db
if DEBUG:
    DATABASES = db.MYSQL
else:
    print('PRODUCCION')
    DATABASES = db.POSTGRES_HEROKU
"""

import dj_database_url
from decouple import config
POSTGRES_HEROKU = {
    'default': dj_database_url.config(
        default = config('DATABASE_URL')
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS':{
            'min_length':8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Guatemala'

USE_I18N = True

USE_TZ = True

# Configuracion para enviar correos electronicos
# settings.py
# DevElTelar30.

# Configuración de correo electrónico
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/code/tpm/email'  # Asegúrate de que este directorio exista.

EMAIL_HOST = 'smtp-mail.outlook.com'  
EMAIL_PORT = 587  
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'DesarrolloElTelar@outlook.com' 
#EMAIL_HOST_PASSWORD = 'tmmbkxogfsvfrimo'
EMAIL_HOST_PASSWORD = 'fmfuzehmqcmrcvqo'
DEFAULT_FROM_EMAIL = 'DesarrolloElTelar@outlook.com'
# UP3HB-9X2AR-YWK8K-UCQCS-Q63T7

# Configuración de Celery
CELERY_BROKER_URL = 'redis://:mystrongpassword@redis:6379/0'  # Usamos Redis como broker
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
#CELERY_TIMEZONE = 'UTC-6'  # Asegúrate de usar la misma zona horaria que tu proyecto Django
CELERY_TIMEZONE = "America/Guatemala"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Configuración de Celery Beat
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'tarea-diaria-a-medianoche': {
        'task': 'apps.financings.task.cambiar_plan',
        'schedule': crontab(minute=0, hour=0),  # A las 00:00 hrs
        'options': {'time_limit': 180},
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Configuración de archivos estáticos y medios

# settings.py

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]

# settings.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'