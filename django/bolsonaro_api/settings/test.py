from .local import *  # pylint:disable=wildcard-import,unused-wildcard-import

DRF_RECAPTCHA_SECRET_KEY = secret("RECAPTCHA_SECRET_KEY", default="")
# https://developers.google.com/recaptcha/docs/faq#id-like-to-run-automated-tests-with-recaptcha.-what-should-i-do
