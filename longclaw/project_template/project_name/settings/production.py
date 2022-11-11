from .base import *  # noqa

DEBUG = False

try:
    from .local import *  # noqa
except ImportError:
    pass
