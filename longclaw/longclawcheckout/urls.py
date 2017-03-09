from django.conf.urls import url
from longclaw.longclawcheckout import api
from longclaw.settings import API_URL_PREFIX

urlpatterns = [
    url(API_URL_PREFIX + r'payment/$',
        api.capture_payment,
        name='payment'),
    url(API_URL_PREFIX + r'create_token/$',
        api.create_token,
        name='create_token')
]