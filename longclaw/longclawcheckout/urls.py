from django.conf.urls import url
from longclaw.longclawcheckout import api
from longclaw.settings import API_URL_PREFIX

urlpatterns = [
    url(API_URL_PREFIX + r'checkout/$',
        api.capture_payment,
        name='longclaw_checkout'),
    url(API_URL_PREFIX + r'checkout/prepaid/$',
        api.create_order_with_token,
        name='longclaw_checkout_prepaid'),
    url(API_URL_PREFIX + r'checkout/token/$',
        api.create_token,
        name='longclaw_checkout_token')
]