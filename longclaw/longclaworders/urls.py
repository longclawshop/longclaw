from django.conf.urls import url
from longclaw.longclaworders import api

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

urlpatterns = [
    url(
        API_URL_PREFIX + r'order/(?P<pk>[0-9]+)/$',
        orders,
        name='longclaw_orders'
    ),

    url(
        API_URL_PREFIX + r'order/(?P<pk>[0-9]+)/fulfill/$',
        fulfill_order,
        name='longclaw_fulfill_order'
    ),

    url(
        API_URL_PREFIX + r'order/(?P<pk>[0-9]+)/refund/$',
        refund_order,
        name='longclaw_refund_order'
    )
]
