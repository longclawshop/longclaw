from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "{{ secret_key }}"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *  # noqa
except ImportError:
    pass
