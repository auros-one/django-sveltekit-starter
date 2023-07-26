"""
Django settings for django-template.
"""

from datetime import timedelta
import os
from pathlib import Path
from urllib.parse import urlparse

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

load_dotenv()
load_dotenv("/app/secrets/.env")

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

# Security.

ALLOWED_HOSTS = ["https://django-template.com", "localhost"]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    # Defaults:
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    # Added for front-end Sentry
    "baggage",
    "sentry-trace",
]

CORS_ALLOWED_ORIGINS = [
    "https://django-template.com",
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "https://django-template.com",
]

DEBUG = os.environ.get("DEBUG") == "1"

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-o4_+-(&c531@xq6a5d1++n*aqt5r08$f*siuahdadskp1sq^"
)

if cloud_run_service_url := os.environ.get("CLOUDRUN_SERVICE_URL"):  # pragma: no cover
    ALLOWED_HOSTS.append(urlparse(cloud_run_service_url).netloc)
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS.append(cloud_run_service_url)
    LANGUAGE_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31_536_000  # One year.
    SESSION_COOKIE_SECURE = True

if ENVIRONMENT == "development":  # pragma: no cover
    CORS_ALLOWED_ORIGINS.append("http://localhost:5173")
    CSP_DEFAULT_SRC = (
        "'self'",
        "'unsafe-inline'",
        "http://localhost:5173",
        "ws://localhost:5173",
    )

PERMISSIONS_POLICY: dict[str, list[str]] = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}


# Application definition.

SITE_ID = 1

APPEND_SLASH = False

AUTH_USER_MODEL = "accounts.User"

INSTALLED_APPS = [
    # Needs to go before other apps.
    "django_template.accounts.apps.AccountsConfig",
    "django_template.utils.apps.UtilsConfig",
    "debug_toolbar",
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_template.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                # Both are required for the django admin app:
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "django_template.wsgi.application"


# DRF

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    )
}
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_REFRESH_COOKIE': 'refresh-token',
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
'USER_DETAILS_SERIALIZER': 'django_template.accounts.serializers.UserDetailsSerializer',
}



# Authentication

OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

# we use email as the primary identifier, not username
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None



# Database.

DATABASES = {
    "default": {
        "CONN_MAX_AGE": None,
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "USER": os.environ.get("POSTGRES_USER"),
    }
}


# Passwords.

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher"]


# Email

if ENVIRONMENT == "development":  # pragma: no cover
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    raise NotImplementedError("Email backend not configured for production.")


# Internationalization.

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True


# Static files.

STATICFILES_DIRS = [BASE_DIR / "django_template" / "static" / "dist"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "/static/"


# Default primary key field type.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# System checks.

SILENCED_SYSTEM_CHECKS = [
    # Username field must be unique -- we use a custom unique constraint.
    "auth.E003",
    # SECURE_SSL_REDIRECT -- seems to break Cloud Run and is handled there.
    "security.W008",
]


# Logging & reporting.

if sentry_dsn := os.environ.get("SENTRY_DSN"):  # pragma: no cover
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=ENVIRONMENT,
        integrations=[DjangoIntegration(), LoggingIntegration()],
        request_bodies="medium",
        send_default_pii=True,
    )


# Debug Toolbar


def show_toolbar(request):  # pragma: no cover
    if DEBUG:
        return True
    user = getattr(request, "user", None)
    if not user:
        return False
    return request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}


# Typing.

try:
    import django_stubs_ext
except ImportError:  # pragma: no cover
    pass
else:
    django_stubs_ext.monkeypatch()
