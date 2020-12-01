from django.conf.urls import url
from longclaw.coupon import views
from longclaw.settings import API_URL_PREFIX

urlpatterns = [
    url(API_URL_PREFIX + r'coupon/verify-discount-code/$',
        views.verify_discount_code,
        name='verify_discount_code'),
    url(API_URL_PREFIX + r'coupon/remove-basket-discount/$',
        views.remove_basket_discount,
        name='remove_basket_discount')
]
