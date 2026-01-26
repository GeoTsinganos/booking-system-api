"""
Django settings for booking_system project.
Production-ready configuration.
"""

from pathlib import Path
import os
from datetime import timedelta

# ======================================================
# Base
# ======================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ======================================================
# Security / Environment
# ======================================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-unsafe") # local fallback ok

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]


# ======================================================
# Application definition
# ======================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",
    "drf_yasg",

    "bookings",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "booking_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "booking_system.wsgi.application"


# ======================================================
# Database (Railway MySQL env vars)
# ======================================================
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
if not MYSQLPASSWORD and DEBUG:
    MYSQLPASSWORD = "Booking123!!!"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQLDATABASE", "booking_db"),
        "USER": os.getenv("MYSQLUSER", "booking_user"),
        "PASSWORD": MYSQLPASSWORD,
        "HOST": os.getenv("MYSQLHOST", "localhost"),
        "PORT": os.getenv("MYSQLPORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4",},
    }
}


# ======================================================
# Password validation
# ======================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ======================================================
# Internationalization
# ======================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True


# ======================================================
# Static files (WhiteNoise)
# ======================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = ("whitenoise.storage.CompressedManifestStaticFilesStorage")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ======================================================
# Django REST Framework / JWT
# ======================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# ======================================================
# Swagger
# ======================================================
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header. Example: "Bearer <token>"',
        }
    }
}

# ======================================================
# CORS (safe defaults)
# ======================================================
cors_env = os.getenv("CORS_ALLOWED_ORIGINS", "")
if cors_env:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in cors_env.split(",") if o.strip()]
else:
    CORS_ALLOWED_ORIGINS = []

# Local dev convenience
if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


CORS_ALLOW_CREDENTIALS = True

csrf_env = os.getenv("CSRF_TRUSTED_ORIGINS", "")
if csrf_env:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_env.split(",") if o.strip()]
