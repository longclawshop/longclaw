from django.conf.urls import url
from django.conf import settings
from longclaw.longclaworders import api

from longclaw.settings import API_URL_PREFIX

orders = api.OrderViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    ### VIEWS ###
    url(
        API_URL_PREFIX + r'order/(?P<pk>[0-9]+)/$',
        orders,
        name='orders'
    ),

    url(
        API_URL_PREFIX + r'order/(?P<pk>[0-9]+)/fulfill/$',
        api.fulfill_order,
        name='fulfill_order'
    )
]

