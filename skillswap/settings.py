# settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
MEDIA_DIR = BASE_DIR / 'media'

# ----- Security & environment -----
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-override-me')
DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

# WEBSITE_HOSTNAME is injected by Azure at runtime
WEBSITE_HOSTNAME = os.environ.get('WEBSITE_HOSTNAME')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if WEBSITE_HOSTNAME:
    ALLOWED_HOSTS.append(WEBSITE_HOSTNAME)

# Required on Azure (Django 4+)
if WEBSITE_HOSTNAME:
    CSRF_TRUSTED_ORIGINS = [f"https://{WEBSITE_HOSTNAME}"]

# ----- Installed apps (keep yours) -----
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    # your apps
    'skills', 'contactapp', 'user_authentication', 'reviewsapp', 'browse',
]

# ----- Middleware (add WhiteNoise right after SecurityMiddleware) -----
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skillswap.urls'
WSGI_APPLICATION = 'skillswap.wsgi.application'

# ----- Database (sqlite is fine for demo) -----
DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}
}

# ----- Static & media (Azure + WhiteNoise) -----
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Keep dev assets if the folder exists locally
if STATIC_DIR.exists():
    STATICFILES_DIRS = [STATIC_DIR]

MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

# WhiteNoise recommended storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Optional: respect reverse proxy HTTPS headers on Azure
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth & login (keep yours)
AUTH_USER_MODEL = 'auth.User'
LOGIN_URL = '/auth/login/'
