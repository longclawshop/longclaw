from django.urls import include, path

from longclaw.basket import urls as basket_urls
from longclaw.checkout import urls as checkout_urls
from longclaw.orders import urls as order_urls
from longclaw.shipping import urls as shipping_urls

urlpatterns = [
    path("", include(basket_urls)),
    path("", include(checkout_urls)),
    path("", include(shipping_urls)),
    path("", include(order_urls)),
]
