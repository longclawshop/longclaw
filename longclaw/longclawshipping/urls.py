from django.conf.urls import url
from longclaw.longclawshipping import api

urlpatterns = [
    url(r'shipping/cost/$',
        api.shipping_cost,
        name='shipping_cost'),
    url(r'shipping/countries/$',
        api.shipping_countries,
        name="shipping_countries")
]
