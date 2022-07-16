"""Django settings."""
from pathlib import Path

from django.contrib.messages import constants as messages
from django.core.management.utils import get_random_secret_key

# General
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "j^)#)4^x5nwol5hs*m7=5zamo8oa5%o%gx!z(^b-8km)60cly2"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Application Definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "corsheaders",
    "auths.apps.AuthsConfig",
    "nutrition.apps.NutritionConfig",
    "fitness.apps.FitnessConfig",
    "trainer.apps.TrainerConfig",
    "forefront.apps.ForefrontConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path.joinpath(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "django.templatetags.static",
                "django.templatetags.i18n",
            ],
        },
    },
]

# Hosting
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "kenko-db",
        "USER": "kenko-user",
        "PASSWORD": "gr@yMask36",
        "HOST": "34.65.58.229",
        "PORT": "5432",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
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
AUTH_USER_MODEL = "auths.User"

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Cairo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/s/"
STATIC_ROOT = Path.joinpath(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    Path.joinpath(BASE_DIR, "static"),
]

# Media (User Files)
MEDIA_URL = "/m/"
MEDIA_ROOT = Path.joinpath(BASE_DIR, "media")

# Messages
MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}
