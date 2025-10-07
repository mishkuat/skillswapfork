# settings.py
from pathlib import Path
import os

# ---------------------------------------------------------
# Base paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
MEDIA_DIR = BASE_DIR / 'media'

# ---------------------------------------------------------
# Security & environment
# ---------------------------------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key')
DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'   # keep True for dev on Azure

# Allow Azure and local hosts
WEBSITE_HOSTNAME = os.environ.get('WEBSITE_HOSTNAME')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if WEBSITE_HOSTNAME:
    ALLOWED_HOSTS.append(WEBSITE_HOSTNAME)
else:
    ALLOWED_HOSTS.append('*')  # dev only

# CSRF (required on Azure)
if WEBSITE_HOSTNAME:
    CSRF_TRUSTED_ORIGINS = [f"https://{WEBSITE_HOSTNAME}"]

# ---------------------------------------------------------
# Application definition
# ---------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # project apps
    'skills',
    'contactapp',
    'user_authentication',
    'reviewsapp',
    'browse',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skillswap.urls'
WSGI_APPLICATION = 'skillswap.wsgi.application'

# ---------------------------------------------------------
# Templates (project-level templates/ + app templates)
# ---------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],      # <project>/templates/
        'APP_DIRS': True,             # <app>/templates/<app>/...
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

# ---------------------------------------------------------
# Database (SQLite – Azure writable path)
# ---------------------------------------------------------
if WEBSITE_HOSTNAME:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/home/site/db/db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ---------------------------------------------------------
# Static & Media (WhiteNoise)
# ---------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
if STATIC_DIR.exists():
    STATICFILES_DIRS = [STATIC_DIR]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

# Respect HTTPS headers from Azure reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ---------------------------------------------------------
# Localization
# ---------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# Default primary key field type
# ---------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------
AUTH_USER_MODEL = 'auth.User'
LOGIN_URL = '/auth/login/'
