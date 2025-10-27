from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Use SECRET_KEY from environment or .env in production. Provide a
# development default to avoid startup errors when a secret isn't set.
SECRET_KEY = config('SECRET_KEY', default='dev-change-me-please-set-in-production')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skika_backend.urls'

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='skika_db'),
        # Use DB_USER/DB_PASSWORD env vars (safer and conventional names).
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Africa's Talking credentials
AFRICASTALKING_USERNAME = config('AFRICASTALKING_USERNAME')
AFRICASTALKING_API_KEY = config('AFRICASTALKING_API_KEY')

# Static files (required by django.contrib.staticfiles)
# See: https://docs.djangoproject.com/en/stable/ref/settings/#static-url
STATIC_URL = '/static/'
# Where `collectstatic` will collect to (useful for deployment)
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Additional locations the staticfiles app will search for static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Africa's Talking credentials
AFRICASTALKING_USERNAME = config('AFRICASTALKING_USERNAME')
AFRICASTALKING_API_KEY = config('AFRICASTALKING_API_KEY')

# Security
# Enable strict security flags when not in DEBUG mode. This avoids
# redirect/cookie issues during local development while still enforcing
# secure settings in production.
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG