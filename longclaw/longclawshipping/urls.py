from django.conf.urls import url
from longclaw.longclawshipping import api
from longclaw.settings import API_URL_PREFIX

urlpatterns = [
    url(API_URL_PREFIX + r'shipping/cost/$',
        api.shipping_cost,
        name='shipping_cost'),
    url(API_URL_PREFIX + r'shipping/countries/$',
        api.shipping_countries,
        name="shipping_countries")
]
