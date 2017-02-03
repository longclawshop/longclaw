from django.conf.urls import url
from checkout import api

urlpatterns = [
    url(r'shipping/$',
        api.shipping_cost,
        name='shipping'),
    url(r'payment/$',
        api.capture_payment,
        name='payment'),
    url(r'create_token/$',
        api.create_token,
        name='create_token')
]