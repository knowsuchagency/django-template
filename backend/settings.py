"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from functools import partial
from pathlib import Path

import sentry_sdk
from corsheaders.defaults import default_headers
from decouple import config
from dj_database_url import parse as db_url
from django.core.management.utils import get_random_secret_key
from loguru import logger
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)
logger.info(f"DEBUG: {DEBUG}")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=str.split)
logger.info(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=str.split)
logger.info(f"CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")

CSRF_COOKIE_DOMAIN = config(
    "CSRF_COOKIE_DOMAIN",
    default=".knowsuchagency.com",
    cast=str,
)
logger.info(f"CSRF_COOKIE_DOMAIN: {CSRF_COOKIE_DOMAIN}")

SESSION_COOKIE_DOMAIN = config(
    "SESSION_COOKIE_DOMAIN",
    default=".knowsuchagency.com",
    cast=str,
)
logger.info(f"SESSION_COOKIE_DOMAIN: {SESSION_COOKIE_DOMAIN}")

CSRF_COOKIE_SETTINGS = config("CSRF_COOKIE_SETTINGS", default="Lax", cast=str)
logger.info(f"CSRF_COOKIE_SETTINGS: {CSRF_COOKIE_SETTINGS}")

CSRF_COOKIE_HTTPONLY = config("CSRF_COOKIE_HTTPONLY", default=False, cast=bool)
logger.info(f"CSRF_COOKIE_HTTPONLY: {CSRF_COOKIE_HTTPONLY}")

LOG_REQUESTS = config("LOG_REQUESTS", default=False, cast=bool)

SENTRY_DSN = config("SENTRY_DSN", default="")

if SENTRY_DSN:
    glitchtip_environment = "development" if DEBUG else "production"
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        auto_session_tracking=False,
        traces_sample_rate=0.01,
        release="1.0.0",
        environment=glitchtip_environment,
    )
    logger.info(f"Sentry initialized for environment: {glitchtip_environment}")
else:
    logger.info("No Glitchtip DSN provided, skipping Sentry initialization")

if DEBUG:
    ALLOWED_HOSTS += ["*"]
    CSRF_COOKIE_DOMAIN = None
    SESSION_COOKIE_DOMAIN = None
    CSRF_TRUSTED_ORIGINS += [
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
    ]
    CORS_ALLOW_CREDENTIALS = True
    CSRF_COOKIE_SECURE = False

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_browser_reload",
    "backend.core",
]

ALLAUTH_APPS = [
    "allauth",
    "allauth.account",
    # "allauth.socialaccount",
    # "allauth.socialaccount.providers.apple",
    # "allauth.socialaccount.providers.google",
    # "allauth.socialaccount.providers.github",
    # "allauth.socialaccount.providers.instagram",
    # "allauth.socialaccount.providers.linkedin",
    # "allauth.socialaccount.providers.microsoft",
]

INSTALLED_APPS += ALLAUTH_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

if DEBUG or LOG_REQUESTS:
    MIDDLEWARE.append("backend.core.middleware.RequestLoggingMiddleware")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
        # set the cache timeout to 30 days
        "TIMEOUT": 60 * 60 * 24 * 30,
    }
}

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASE_URL = config(
    "DATABASE_URL",
    default="sqlite:///" + str(BASE_DIR / "db.sqlite3"),
    cast=partial(
        db_url,
        conn_max_age=600,
        conn_health_checks=True,
    ),
)

DATABASES = {
    "default": DATABASE_URL,
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS settings

# For development (allow all origins):
CORS_ALLOW_ALL_ORIGINS = DEBUG
logger.info(f"CORS_ALLOW_ALL_ORIGINS: {CORS_ALLOW_ALL_ORIGINS}")

# For production (specify allowed origins):
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="", cast=str.split)
# assume our frontend should be able to make POST requests and fetch content from its domain
CORS_ALLOWED_ORIGINS += CSRF_TRUSTED_ORIGINS
logger.info(f"CORS_ALLOWED_ORIGINS: {CORS_ALLOWED_ORIGINS}")

# If you need to allow credentials (cookies, authorization headers, etc.):
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    *default_headers,
    "x-session-token",
    "content-type",
    "x-csrftoken",
)
logger.info(f"CORS_ALLOW_HEADERS: {CORS_ALLOW_HEADERS}")

CORS_EXPOSE_HEADERS = [
    "content-type",
    "x-session-token",
    "x-csrftoken",
]
logger.info(f"CORS_EXPOSE_HEADERS: {CORS_EXPOSE_HEADERS}")

# Auth settings

AUTH_USER_MODEL = "core.User"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Email settings

EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
EMAIL_HOST = "email-smtp.us-east-2.amazonaws.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("AWS_ACCESS_KEY_ID", default="")
EMAIL_HOST_PASSWORD = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_DEFAULT_REGION = os.environ["AWS_DEFAULT_REGION"] = config(
    "AWS_DEFAULT_REGION", default="us-east-2"
)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@knowsuchagency.com")

# Authentication settings
LOGIN_REDIRECT_URL = "/"  # Redirect to landing page after login
LOGOUT_REDIRECT_URL = "/"  # Redirect to landing page after logout
LOGIN_URL = "/accounts/login/"  # Where to redirect if login is required

# Security settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = not DEBUG
