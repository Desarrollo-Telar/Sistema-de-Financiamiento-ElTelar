
from pathlib import Path
import os.path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f(l@4iukkrz%^l92ant-7xc4s%k1l%u_5a^#e3(f%3wi*3lutw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SERVIDOR = True
ALLOWED_HOSTS = ['*']


# Application definition
from .apps_instaladas import INSTALLED_APPS_MODELS, INSTALLED_APPS_REST

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'crispy_forms',
    'coreapi', 
    'django_celery_beat',
    'django.contrib.sites',
    'django_redis',
    'storages',
    'modelos',  
]
INSTALLED_APPS += INSTALLED_APPS_MODELS + INSTALLED_APPS_REST
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise 
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # MIDDLEWARE 
    'project.middleware.AutoLogoutMiddleware',
    'project.middleware.RestrictedAccessByTimeMiddleware',
    'project.middleware.UserActionLoggingMiddleware',
    
]

# Modo de mantenimiento
MAINTENANCE_MODE = False  # Cambia a False para desactivar el modo de mantenimiento

# Configura el tiempo de expiración de la sesión a 45 minutos
SESSION_COOKIE_AGE = 2700  # 45 minutos en segundos

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

# ------------------------------------------------------------------------ #
SIMPLE_JWT = {
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
}


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# ------------------------------------------------------------------------ #

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
                'django.template.context_processors.request', 
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

import project.database as db



_database = db.POSTGRES_HEROKU

if not SERVIDOR:
    _database = db.POSTGRES


DATABASES = _database




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
# nifs xjvc fbvo jxav
# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'develtelar@gmail.com'
EMAIL_HOST_PASSWORD = 'nifs xjvc fbvo jxav'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Configuración de Celery

CELERY_BROKER_URL = 'redis://:mystrongpassword@redis:6379/0'  # Usamos Redis como broker
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

#CELERY_TIMEZONE = 'UTC-6'  # Asegúrate de usar la misma zona horaria que tu proyecto Django
CELERY_TIMEZONE = "America/Guatemala"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Configuración de Celery Beat
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

from celery.schedules import crontab

from urllib.parse import urlparse
#REDISCLOUD_URL = 'redis://default:PTSGV1jP5KdITaOQxjLZotZZyG623CGf@redis-12001.c52.us-east-1-4.ec2.redns.redis-cloud.com:12001'

"""
redis_url = urlparse(os.environ.get('REDISCLOUD_URL'))
CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
            'OPTIONS': {
                'PASSWORD': redis_url.password,
                'DB': 0,
        }
    }
}
""" 
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDISCLOUD_URL", "redis://redis:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

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
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


AWS_ACCESS_KEY_ID = "WkXu9MHvOHvOsLiJjtda"  # Cambia según tu configuración
AWS_SECRET_ACCESS_KEY = "g75dCPXZlgogk0KloBAM1BI2SfaqzDp2ufciMrIe"
AWS_STORAGE_BUCKET_NAME = "asiatrip"
AWS_S3_ENDPOINT_URL = "https://pcxl65.stackhero-network.com"  # Reemplaza con la URL de tu MinIO
AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


