from django.conf.urls import url
from longclaw.longclawcheckout import api

urlpatterns = [
    url(r'payment/$',
        api.capture_payment,
        name='payment'),
    url(r'create_token/$',
        api.create_token,
        name='create_token')
]