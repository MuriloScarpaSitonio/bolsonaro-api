import os

from decouple import config as secret

from .base import *  # pylint:disable=wildcard-import,unused-wildcard-import

REACT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "react"))

TEMPLATES[0]["DIRS"] += [os.path.join(REACT_DIR, "build")]  # type: ignore

DATABASES = {
    "default": {
        "ENGINE": secret("DATABASE_ENGINE", default="django.db.backends.sqlite3"),
        "PORT": secret("DATABASE_PORT", cast=int, default=5432),
        "USER": secret("DATABASE_USER", default="user"),
        "NAME": secret("DATABASE_NAME", default=BASE_DIR / "db.sqlite3"),
        "PASSWORD": secret("DATABASE_PASSWORD", default="password"),
        "HOST": secret("DATABASE_HOST", default="localhost"),
    }
}

STATICFILES_DIRS = (os.path.join(REACT_DIR, "build", "static"),)

DRF_RECAPTCHA_SECRET_KEY = secret(
    "RECAPTCHA_SECRET_KEY", default="6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
)
# https://developers.google.com/recaptcha/docs/faq#id-like-to-run-automated-tests-with-recaptcha.-what-should-i-do
