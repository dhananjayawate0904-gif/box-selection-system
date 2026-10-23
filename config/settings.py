"""Django settings for the local box-selection application."""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
debug_default = "false" if render_hostname else "true"
DEBUG = os.environ.get("DEBUG", debug_default).strip().lower() in {
    "true",
    "1",
    "yes",
}
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            "Set DJANGO_SECRET_KEY to a private value when DEBUG is disabled."
        )
    SECRET_KEY = "django-insecure-local-development-only-change-before-deployment"

configured_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [
    host.strip()
    for host in configured_hosts.split(",")
    if host.strip()
]
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
if DEBUG:
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1"])
elif not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "Set RENDER_EXTERNAL_HOSTNAME or DJANGO_ALLOWED_HOSTS when DEBUG is disabled."
    )

csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in csrf_origins.split(",")
    if origin.strip()
]
if render_hostname:
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_hostname}")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "boxes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
