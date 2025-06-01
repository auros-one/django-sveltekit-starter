"""
Django settings
"""

import logging
import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

import dj_database_url
import nest_asyncio
import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

logger = logging.getLogger(__name__)


load_dotenv()
load_dotenv("/app/secrets/.env", override=True)  # .env is here in production

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")


# Domains

HOST_DOMAINS = os.environ.get("HOST_DOMAINS", "localhost:8000, 127.0.0.1").split(",")
FRONTEND_DOMAINS = os.environ.get("FRONTEND_DOMAINS", "localhost:5173").split(",")

PASSWORD_CONFIRM_RESET_PATH = os.environ.get(
    "PASSWORD_RESET_PATH", "/account/reset-password/confirm"
)
EMAIL_VERIFICATION_PATH = os.environ.get(
    "EMAIL_VERIFICATION_PATH", "/account/verify-email"
)


# Security

ALLOWED_HOSTS = HOST_DOMAINS

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
    f"https://{domain}" for domain in HOST_DOMAINS + FRONTEND_DOMAINS if domain
]

CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

DEBUG = os.environ.get("DEBUG") == "1"

SECRET_KEY = os.environ.get("SECRET_KEY", None)
if ENVIRONMENT == "production" and SECRET_KEY is None:  # pragma: no cover
    raise Exception("SECRET_KEY must be set in production.")
else:
    SECRET_KEY = "django-insecure-o4_+-(&c531@xq6a5d1++n*aqt5r08$f*siuahdadskp1sq^"

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_SECONDS = 60  # TODO: after confirming this works in production, change this to: 31_536_000  # One year.

SESSION_COOKIE_SECURE = True

LANGUAGE_COOKIE_SECURE = True

if cloud_run_service_url := os.environ.get("CLOUDRUN_SERVICE_URL"):  # pragma: no cover
    ALLOWED_HOSTS.append(urlparse(cloud_run_service_url).netloc)
    CSRF_TRUSTED_ORIGINS.append(cloud_run_service_url)

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
    SECURE_HSTS_SECONDS = 0

CSP_SCRIPT_SRC = [
    "'self'",
    "blob:",
    "cdn.jsdelivr.net",
]

CSP_STYLE_SRC = [
    "'self'",
    "cdn.jsdelivr.net",
    "'unsafe-inline'",
]


# Application definition.

SITE_ID = 1

APPEND_SLASH = True

AUTH_USER_MODEL = "accounts.User"

INSTALLED_APPS = [
    # Needs to go before other apps.
    "project.accounts.apps.AccountsConfig",
    "project.core.apps.CoreConfig",
    "project.apps.CustomAdminConfig",
    "corsheaders",
    "debug_toolbar",
    "django_extensions",
    "django_celery_beat",
    "revproxy.apps.RevProxyConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "drf_spectacular",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "anymail",
    "dj_rest_auth.registration",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "project.core.xframe.XFrameAllowFrontendDomainsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
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
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_REFRESH_COOKIE": "refresh-token",
    "USER_DETAILS_SERIALIZER": "project.accounts.serializers.UserDetailsSerializer",
    "PASSWORD_RESET_SERIALIZER": "project.accounts.serializers.PasswordResetSerializer",
    "OLD_PASSWORD_FIELD_ENABLED": True,
}

# django-allauth (dj-rest-auth uses django-allauth under the hood.)
ACCOUNT_ADAPTER = "project.accounts.adapters.CustomAccountAdapter"
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""

SIMPLE_JWT = {
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}

if ENVIRONMENT == "production":  # pragma: no cover
    REST_AUTH["JWT_AUTH_SAMESITE"] = "None"
    REST_AUTH["JWT_AUTH_SECURE"] = True


# drf-spectacular

SPECTACULAR_SETTINGS = {
    "TITLE": "API Documentation",
    "VERSION": "0.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Split request and response schemas otherwise most client-generators will fail.
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": "/api",
    "SCHEMA_PATH_PREFIX_TRIM": True,
    "TAGS": [
        {
            "name": "Checks",
            "description": "Utility endpoints for checking the usability of the API.",
        }
    ],
}


# Authentication

OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

# we use email as the primary identifier, not username
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None


# Database.

if database_url := os.environ.get("DATABASE_URL"):
    DATABASES = {"default": dj_database_url.parse(database_url)}
else:
    DATABASES = {
        "default": {
            "CONN_MAX_AGE": 0,
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
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


# Logging & reporting.

if sentry_dsn := os.environ.get("SENTRY_DSN"):  # pragma: no cover
    # Only initialize Sentry if DSN is not empty
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=ENVIRONMENT,
        integrations=[DjangoIntegration(), LoggingIntegration()],
        max_request_body_size="medium",
        send_default_pii=True,
    )
else:
    logger.info("Sentry DSN is empty, skipping Sentry initialization")


# Email

# default email settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@localhost"  # used by django-allauth when sending emails

# in production, try to use Mailgun.
if ENVIRONMENT == "production":  # pragma: no cover
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    MAILGUN_SENDER_DOMAIN = os.environ.get("MAILGUN_SENDER_DOMAIN")
    if (
        MAILGUN_API_KEY is None
        or MAILGUN_API_KEY == ""
        or MAILGUN_SENDER_DOMAIN is None
        or MAILGUN_SENDER_DOMAIN == ""
    ):
        logger.error(
            "MAILGUN_API_KEY and MAILGUN_SENDER_DOMAIN must be set in production. Falling back to console EmailBackend."
        )
    else:
        EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
        DEFAULT_FROM_EMAIL = (
            "no-reply@"
            + MAILGUN_SENDER_DOMAIN  # used by django-allauth when sending emails
        )

SERVER_EMAIL = DEFAULT_FROM_EMAIL


# Internationalization.

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True


# Static files.

STATICFILES_DIRS = [BASE_DIR / "project" / "core" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/api/static/"

if ENVIRONMENT == "production":  # pragma: no cover
    # S3 Storage Settings for Hetzner
    HETZNER_ACCESS_KEY_ID = os.environ.get("HETZNER_S3_ACCESS_KEY")
    HETZNER_SECRET_ACCESS_KEY = os.environ.get("HETZNER_S3_SECRET_KEY")
    HETZNER_STORAGE_BUCKET_NAME = os.environ.get("HETZNER_S3_BUCKET_NAME")
    HETZNER_S3_ENDPOINT_URL = os.environ.get("HETZNER_S3_ENDPOINT_URL")
    HETZNER_S3_REGION_NAME = os.environ.get("HETZNER_S3_REGION_NAME")
    HETZNER_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    HETZNER_DEFAULT_ACL = "public-read"
    HETZNER_QUERYSTRING_AUTH = False

    # Storage backends
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "bucket_name": HETZNER_STORAGE_BUCKET_NAME,
                "location": "media",
                "access_key": HETZNER_ACCESS_KEY_ID,
                "secret_key": HETZNER_SECRET_ACCESS_KEY,
                "region_name": HETZNER_S3_REGION_NAME,
                "endpoint_url": HETZNER_S3_ENDPOINT_URL,
                "default_acl": HETZNER_DEFAULT_ACL,
                "querystring_auth": HETZNER_QUERYSTRING_AUTH,
                "object_parameters": HETZNER_S3_OBJECT_PARAMETERS,
                "addressing_style": "path",
                "signature_version": "s3",
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    # Media URL for production
    MEDIA_URL = f"{HETZNER_S3_ENDPOINT_URL}/{HETZNER_STORAGE_BUCKET_NAME}/media/"
else:
    # Local storage settings.
    default_storage_path = BASE_DIR / "storage/"
    if not default_storage_path.exists():  # pragma: no cover
        default_storage_path.mkdir(mode=0o700)  # TODO is this necessary ??

    # Storages settings for development
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": str(default_storage_path),
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        },
    }

    # Media URL for development
    MEDIA_URL = "/media/"

# Redis and Celery Settings
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", REDIS_URL)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# Default primary key field type.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# System checks.

SILENCED_SYSTEM_CHECKS = [
    # Username field must be unique -- we use a custom unique constraint.
    "auth.E003",
    # SECURE_SSL_REDIRECT -- seems to break Cloud Run and is handled there.
    "security.W008",
    # we don't use django.middleware.csrf.CsrfViewMiddleware, instead we
    # use our custom project.core.middleware.CsrfProtectMiddleware that
    # only applies to the admin and debug toolbar.
    "security.W003",
]
if ENVIRONMENT == "development":  # pragma: no cover
    SILENCED_SYSTEM_CHECKS.extend(
        [
            "security.W004",  # SECURE_HSTS_SECONDS
            "security.W009",  # SECRET_KEY
            "security.W018",  # DEBUG
        ]
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


# Dokku
DOKKU_APP_NAME = os.environ.get("DOKKU_APP_NAME")


# Prevent some asyncio issues
# https://github.com/erdewit/nest_asyncio
nest_asyncio.apply()
