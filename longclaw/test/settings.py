# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

import os

from wagtail import VERSION as WAGTAIL_VERSION

# import sys


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"

# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

# if "test" in sys.argv:
#     sys.stdout.write("*** Using in-memory sqlite database for tests ***\n")
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": ":memory:",
#         },
#     }
# else:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "test_longclaw_db.sqlite3"),
    },
}

ROOT_URLCONF = "longclaw.test.urls"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.styleguide",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail" if WAGTAIL_VERSION >= (3, 0) else "wagtail.core",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "modelcluster",
    "taggit",
    "rest_framework",
    "django_extensions",
    "longclaw.core",
    "longclaw.configuration",
    "longclaw.shipping",
    "longclaw.products",
    "longclaw.orders",
    "longclaw.checkout",
    "longclaw.basket",
    "longclaw.stats",
    "longclaw.test",
    "longclaw.contrib.productrequests",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.legacy.sitemiddleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(os.path.dirname(__file__), "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "longclaw.configuration.context_processors.currency",
            ],
        },
    },
]

STATIC_URL = "/static/"

PRODUCT_VARIANT_MODEL = "longclaw_test.ProductVariant"

# DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

WAGTAILADMIN_BASE_URL = "http://localhost:8000/admin"

WAGTAIL_SITE_NAME = "Longclaw"

# Internationalization
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

# USE_TZ = True
