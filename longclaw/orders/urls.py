from django.urls import path

from longclaw.orders import api
from longclaw.settings import API_URL_PREFIX

orders = api.OrderViewSet.as_view({"get": "retrieve"})

fulfill_order = api.OrderViewSet.as_view({"post": "fulfill_order"})

refund_order = api.OrderViewSet.as_view({"post": "refund_order"})

PREFIX = f"{API_URL_PREFIX}order/"
urlpatterns = [
    path(PREFIX + "<pk>/", orders, name="longclaw_orders"),
    path(PREFIX + "<pk>/fulfill/", fulfill_order, name="longclaw_fulfill_order"),
    path(PREFIX + "<pk>/refund/", refund_order, name="longclaw_refund_order"),
]
