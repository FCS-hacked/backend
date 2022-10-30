"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

from corsheaders.defaults import default_headers
from cryptography.hazmat.primitives import serialization

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vm8bt&ctyu@fb#s7zd+&uf8!cxfs18naz4w8#)u0*_5xbup7c)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    "corsheaders",
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'authentication',
    'documents',
    'unauth',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'unauth.drf_custom_authentication.UnauthAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '100/day',
    #     'user': '1000/day'
    # }
}

REST_USE_JWT = True

SPECTACULAR_SETTINGS = {
    'TITLE': 'Hacked',
    'DESCRIPTION': 'Hacked',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_AUTHENTICATION': ['rest_framework.authentication.SessionAuthentication'],
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'COMPONENT_SPLIT_REQUEST': True,
    'SERVE_PUBLIC': True,
    # OTHER SETTINGS
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("GMAIL_ID", "hackedfcsdummy@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "lypsjqeljisphrun")

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "hotp",
]

# JWT_PUBLIC_KEY = b"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDQ/b8C5exroeT5eZVE2fbTnpsa5vjg4O5pCCSCzhUJ52pkxjyQUdV/W5XyziV4YcrMOLKQZzK68V/khpR3fTBVtP4UVjppqjiyl9sIXqRRwAX/EZM9EPJw6Me5DFduifczcPJzjrcnDns3Ni7puUkN7S5jCVFIgyn6mrXJ5m1EYfCLHH86ehsHQ21fE43IFQwPdfg1itlsW/rLJVZhJs666+L50g8iv+hC2r6S1eEsqmteLEDSSxz5b5+SMUOKmdlzxgRXAhK7xOjdz0brRoIb8SWk7Bu7ZLK091XVdrXFj0iotJ77orzhpcQfNflCGRfjMRvSKjW2giOJLlGhw/ryCtOcKL7UUzpaQ9GvReAdfK5ubTZBFjTFF7QwmZbl6s6UZleUNq0MifGqlE1434G8DYfp9kPSui3x8Q/4OUJzYF2DNLVzwaYouftlBwShCWGP4nNW2yIARy5oAqTIfGzN+xCVGKlCQKPrIbsdHIoed41CsCtYukUCf19a8TFtjwE= fitz@c3po"
_JWT_PRIVATE_KEY = b"-----BEGIN OPENSSH PRIVATE KEY-----\n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\n-----END OPENSSH PRIVATE KEY-----"
_JWT_PUBLIC_KEY = b"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDQ/b8C5exroeT5eZVE2fbTnpsa5vjg4O5pCCSCzhUJ52pkxjyQUdV/W5XyziV4YcrMOLKQZzK68V/khpR3fTBVtP4UVjppqjiyl9sIXqRRwAX/EZM9EPJw6Me5DFduifczcPJzjrcnDns3Ni7puUkN7S5jCVFIgyn6mrXJ5m1EYfCLHH86ehsHQ21fE43IFQwPdfg1itlsW/rLJVZhJs666+L50g8iv+hC2r6S1eEsqmteLEDSSxz5b5+SMUOKmdlzxgRXAhK7xOjdz0brRoIb8SWk7Bu7ZLK091XVdrXFj0iotJ77orzhpcQfNflCGRfjMRvSKjW2giOJLlGhw/ryCtOcKL7UUzpaQ9GvReAdfK5ubTZBFjTFF7QwmZbl6s6UZleUNq0MifGqlE1434G8DYfp9kPSui3x8Q/4OUJzYF2DNLVzwaYouftlBwShCWGP4nNW2yIARy5oAqTIfGzN+xCVGKlCQKPrIbsdHIoed41CsCtYukUCf19a8TFtjwE= fitz@c3po"

RSA_private_key_obj = serialization.load_ssh_private_key(_JWT_PRIVATE_KEY, password=None)
RSA_public_key_obj = serialization.load_ssh_public_key(_JWT_PUBLIC_KEY)
