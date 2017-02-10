from django.conf.urls import url
from django.conf import settings

# signals imported so that the post save receivers run..
from longclaw.orders import api

# Bookings
orders = api.OrderViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = (
    ### VIEWS ###
    url(
        r'^order/(?P<pk>[0-9]+)/$',
        orders,
        name='orders'
    ),

    url(
        r'^order/(?P<pk>[0-9]+)/fulfill/$',
        api.fulfill_order,
        name='fulfill_order'
    )
)
