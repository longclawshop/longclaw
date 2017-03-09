from django.conf.urls import include, url
from longclaw.longclawbasket import urls as basket_urls
from longclaw.longclawcheckout import urls as checkout_urls
from longclaw.longclawshipping import urls as shipping_urls
from longclaw.longclaworders import urls as order_urls

urlpatterns = [
    url(r'', include(basket_urls)),
    url(r'', include(checkout_urls)),
    url(r'', include(shipping_urls)),
    url(r'', include(order_urls)),
]
