import os

from decouple import config as secret

from .base import *  # pylint:disable=wildcard-import,unused-wildcard-import

REACT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "react"))

TEMPLATES[0]["DIRS"] += [os.path.join(REACT_DIR, "build")]  # type: ignore

STATICFILES_DIRS = (os.path.join(REACT_DIR, "build", "static"),)

DRF_RECAPTCHA_SECRET_KEY = secret(
    "RECAPTCHA_SECRET_KEY", default="6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
)
# https://developers.google.com/recaptcha/docs/faq#id-like-to-run-automated-tests-with-recaptcha.-what-should-i-do
