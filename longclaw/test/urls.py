# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.urls import include, path
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin import urls as admin_urls

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import urls as wagtail_urls
else:
    from wagtail.core import urls as wagtail_urls

from wagtail.documents import urls as documents_urls

from longclaw import urls as longclaw_urls
from longclaw.contrib.productrequests import urls as request_urls

urlpatterns = [
    path("admin/", include(admin_urls)),
    path("documents/", include(documents_urls)),
    path("", include(longclaw_urls)),
    path("", include(request_urls)),
    path("", include(wagtail_urls)),
]
