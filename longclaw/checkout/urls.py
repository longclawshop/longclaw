from django.urls import path

from longclaw.checkout import api, views
from longclaw.settings import API_URL_PREFIX

urlpatterns = [
    path(API_URL_PREFIX + "checkout/", api.capture_payment, name="longclaw_checkout"),
    path(
        API_URL_PREFIX + "checkout/prepaid/",
        api.create_order_with_token,
        name="longclaw_checkout_prepaid",
    ),
    path(
        API_URL_PREFIX + "checkout/token/",
        api.create_token,
        name="longclaw_checkout_token",
    ),
    path("checkout/", views.CheckoutView.as_view(), name="longclaw_checkout_view"),
    path(
        "checkout/success/<pk>/",
        views.checkout_success,
        name="longclaw_checkout_success",
    ),
]
