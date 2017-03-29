# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from longclaw.longclawbasket.urls import urlpatterns as basket_urls
from longclaw.longclawcheckout.urls import urlpatterns as checkout_urls

urlpatterns = [
    url(r'', include(basket_urls)),
    url(r'', include(checkout_urls)),
]
