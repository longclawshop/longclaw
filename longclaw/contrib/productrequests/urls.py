from django.conf.urls import url
from longclaw.contrib.productrequests import api, views
from longclaw.settings import API_URL_PREFIX

request_list = api.ProductRequestViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

request_detail = api.ProductRequestViewSet.as_view({
    'get': 'retrieve'
})

request_variant = api.ProductRequestViewSet.as_view({
    'get': 'requests_for_variant'
})

urlpatterns = [
    url(
        API_URL_PREFIX + r'requests/$',
        request_list,
        name='productrequests_list'
    ),
    url(
        API_URL_PREFIX + r'requests/(?P<pk>[0-9]+)/$',
        request_detail,
        name='productrequests_detail'
    ),
    url(
        API_URL_PREFIX + r'requests/variant/(?P<variant_id>[0-9]+)/$',
        request_variant,
        name='productrequests_variant_list'
    ),
    url(r'requests/product/(?P<pk>[0-9]+)/$',
        views.requests_admin,
        name='productrequests_admin')
]
