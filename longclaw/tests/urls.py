# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from longclaw.longclawbasket.urls import urlpatterns as basket_urls
from longclaw.longclawcheckout.urls import urlpatterns as checkout_urls
from longclaw.longclawshipping.urls import urlpatterns as shipping_urls
from longclaw.longclaworders.urls import urlpatterns as orders_urls

urlpatterns = [
    url(r'', include(basket_urls)),
    url(r'', include(checkout_urls)),
    url(r'', include(shipping_urls)),
    url(r'', include(orders_urls))
]
