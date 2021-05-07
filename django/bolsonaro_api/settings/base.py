import os
from pathlib import Path

from decouple import Csv, config as secret

if "RDS_DB_NAME" in os.environ:
    from scripts.set_env_vars import set_env_vars

    set_env_vars()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret(
    "DAJNGO_SECRET_KEY", default="2x$e%!k_u_0*gq0s4!_u(2(^lpy&gir0hg)q&5nurj0-sseuav"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = secret("DJANGO_DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = secret("ALLOWED_HOSTS", default="127.0.0.1", cast=Csv())


# Application definition

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "quotes.apps.QuotesConfig",
    "actions.apps.ActionsConfig",
]

THIRD_PARTY_APPS = [
    "taggit",
    "taggit_labels",
    "rest_framework",
    "corsheaders",
    "drf_recaptcha",
    "django_filters",
    "drf_yasg",
]


INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bolsonaro_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "static" / "templates"],
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


WSGI_APPLICATION = "bolsonaro_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%d/%m/%Y %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {"django": {"handlers": ["console"]}},
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATE_INPUT_FORMATS = ["%d/%m/%Y"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

EMAIL_HOST_USER = secret("EMAIL_HOST_USER", default="")
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = secret("SENDGRID_API_KEY", default="")
SENDGRID_SANDBOX_MODE_IN_DEBUG = secret(
    "SENDGRID_SANDBOX_MODE_IN_DEBUG", cast=bool, default=True
)


LANGUAGE_CODE = "pt-br"
CORS_ALLOW_ALL_ORIGINS = True


REST_FRAMEWORK = {
    "DATE_INPUT_FORMATS": ["%d/%m/%Y"],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"anon": "100000/day"},
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


TWITTER_API_KEY = secret("TWITTER_API_KEY", default="")
TWITTER_API_SECRET_KEY = secret("TWITTER_API_SECRET_KEY", default="")
TWITTER_API_TOKEN = secret("TWITTER_API_TOKEN", default="")
TWITTER_API_SECRET_TOKEN = secret("TWITTER_API_SECRET_TOKEN", default="")

CELERY_BROKER_URL = secret("REDIS_URL", default="redis://localhost:6379")
CELERY_RESULT_BACKEND = secret("REDIS_URL", default="redis://localhost:6379")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

SWAGGER_SETTINGS = {"USE_SESSION_AUTH": False}
