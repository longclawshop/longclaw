from django.conf.urls import include, url
from longclaw.basket import urls as basket_urls
from longclaw.checkout import urls as checkout_urls
from longclaw.shipping import urls as shipping_urls
from longclaw.orders import urls as order_urls

urlpatterns = [
    url(r'', include(basket_urls)),
    url(r'', include(checkout_urls)),
    url(r'', include(shipping_urls)),
    url(r'', include(order_urls)),
]
