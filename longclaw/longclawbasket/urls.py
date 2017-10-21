from django.conf.urls import url
from longclaw.longclawbasket import api
from longclaw.longclawbasket import views
from longclaw.settings import API_URL_PREFIX

basket_list = api.BasketViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'bulk_update'
})

basket_detail = api.BasketViewSet.as_view({
    'delete': 'destroy'
})

item_count = api.BasketViewSet.as_view({
    'get': 'item_count'
})

total_items = api.BasketViewSet.as_view({
    'get': 'total_items'
})

urlpatterns = [

    url(API_URL_PREFIX + r'basket/$',
        basket_list,
        name='longclaw_basket_list'),
    url(API_URL_PREFIX + r'basket/count/$',
        total_items,
        name="longclaw_basket_total_items"),
    url(API_URL_PREFIX + r'basket/(?P<variant_id>[0-9]+)/$',
        basket_detail,
        name='longclaw_basket_detail'),
    url(API_URL_PREFIX + r'basket/(?P<variant_id>[0-9]+)/count/$',
        item_count,
        name='longclaw_basket_item_count'),

    url(r'basket/$',
        views.BasketView.as_view(),
        name="longclaw_basket")
]
