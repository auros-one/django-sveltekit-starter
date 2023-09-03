"""
Django settings
"""

import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

import openai
import sentry_sdk
from dotenv import load_dotenv
from google.oauth2 import service_account
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")


# Domains

HOST_DOMAIN = os.environ.get("HOST_DOMAIN", "localhost:8000")
FRONTEND_DOMAINS = os.environ.get("FRONTEND_DOMAINS", "localhost:5173").split(",")


# Security

ALLOWED_HOSTS = (
    [f"{HOST_DOMAIN}"] if ENVIRONMENT == "production" else ["localhost", "127.0.0.1"]
)

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
    f"https://{HOST_DOMAIN}",
] + [f"https://{frontend_domain}" for frontend_domain in FRONTEND_DOMAINS]

CSRF_TRUSTED_ORIGINS = [
    f"https://{HOST_DOMAIN}",
] + [f"https://{frontend_domain}" for frontend_domain in FRONTEND_DOMAINS]

DEBUG = os.environ.get("DEBUG") == "1"

SECRET_KEY = os.environ.get("SECRET_KEY", None)
if ENVIRONMENT == "production" and SECRET_KEY is None:  # pragma: no cover
    raise Exception("SECRET_KEY must be set in production.")
else:
    SECRET_KEY = "django-insecure-o4_+-(&c531@xq6a5d1++n*aqt5r08$f*siuahdadskp1sq^"


SESSION_COOKIE_SECURE = True if ENVIRONMENT == "production" else False
CSRF_COOKIE_SECURE = True if ENVIRONMENT == "production" else False

if ENVIRONMENT == "development":
    CORS_ORIGIN_ALLOW_ALL = True
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS.append("http://localhost:5173")
    CSP_DEFAULT_SRC = (
        "'self'",
        "'unsafe-inline'",
        "http://localhost:5173",
        "ws://localhost:5173",
    )

if cloud_run_service_url := os.environ.get("CLOUDRUN_SERVICE_URL"):  # pragma: no cover
    ALLOWED_HOSTS.append(urlparse(cloud_run_service_url).netloc)
    CSRF_TRUSTED_ORIGINS.append(cloud_run_service_url)
    LANGUAGE_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 60  # TODO: after confirming this works in production, change this to: 31_536_000  # One year.

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
    "project.accounts.apps.AccountsConfig",
    "project.utils.apps.UtilsConfig",
    "corsheaders",
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
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "project.utils.middleware.CsrfProtectMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

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

WSGI_APPLICATION = "project.wsgi.application"


# DRF

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_REFRESH_COOKIE": "refresh-token",
    "USER_DETAILS_SERIALIZER": "project.accounts.serializers.UserDetailsSerializer",
}
SIMPLE_JWT = {
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}

if ENVIRONMENT == "production":  # pragma: no cover
    REST_AUTH["JWT_AUTH_SAMESITE"] = "None"
    REST_AUTH["JWT_AUTH_SECURE"] = True


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

if ENVIRONMENT == "production":
    EMAIL_BACKEND = "django_mailgun.MailgunBackend"
    MAILGUN_ACCESS_KEY = os.environ.get("MAILGUN_ACCESS_KEY")
    MAILGUN_SERVER_NAME = os.environ.get("MAILGUN_SERVER_NAME")
else:  # pragma: no cover
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Internationalization.

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True


# Static files.

STATIC_URL = "/static/"

if ENVIRONMENT == "production":
    # Google Cloud Storage settings.
    STORAGES = {
        "default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"},
        "staticfiles": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"},
    }
    GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        "google_storage_credentials.json"
    )
    STATIC_ROOT = "static"
else:
    # Local storage settings.
    STATICFILES_DIRS = [
        BASE_DIR / "project" / "static"
    ]  # directories where Django will look for static files
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    STATIC_ROOT = (
        BASE_DIR / "staticfiles"
    )  # directory where collectstatic will gather static files


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
        request_bodies="medium",  # type: ignore
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


# OpenAI

if openai_key := os.environ.get("OPENAI_API_KEY"):
    openai.api_key = openai_key
else:  # pragma: no cover
    if ENVIRONMENT == "production":
        raise ValueError("OPENAI_API_KEY not set")

# Helicone (https://www.helicone.ai)

HELICONE_API_KEY = os.environ.get("HELICONE_API_KEY", None)

if HELICONE_API_KEY:
    openai.api_base = "https://oai.hconeai.com/v1"
