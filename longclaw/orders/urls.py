from django.conf.urls import url
from longclaw.orders import api

from longclaw.settings import API_URL_PREFIX

orders = api.OrderViewSet.as_view({
    'get': 'retrieve'
})

fulfill_order = api.OrderViewSet.as_view({
    'post': 'fulfill_order'
})

refund_order = api.OrderViewSet.as_view({
    'post': 'refund_order'
})

PREFIX = r'^{}order/'.format(API_URL_PREFIX)
urlpatterns = [
    url(
        PREFIX + r'(?P<pk>[0-9]+)/$',
        orders,
        name='longclaw_orders'
    ),

    url(
        PREFIX + r'(?P<pk>[0-9]+)/fulfill/$',
        fulfill_order,
        name='longclaw_fulfill_order'
    ),

    url(
        PREFIX + r'(?P<pk>[0-9]+)/refund/$',
        refund_order,
        name='longclaw_refund_order'
    )
]
