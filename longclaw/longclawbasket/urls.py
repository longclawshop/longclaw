from django.conf.urls import url
from longclaw.longclawbasket import api
from longclaw.longclawbasket import views
from longclaw.settings import API_URL_PREFIX

urlpatterns = [
    url(API_URL_PREFIX + r'add_to_basket/$',
        api.add_to_basket,
        name="add_to_basket"),
    url(API_URL_PREFIX + r'remove_from_basket/$',
        api.remove_from_basket,
        name="remove_from_basket"),
    url(API_URL_PREFIX + r'get_item_count/$',
        api.get_item_count,
        name="get_item_count"),
    url(API_URL_PREFIX + r'basket_total_items/$',
        api.basket_total_items,
        name="basket_total_items"),
    url(API_URL_PREFIX + r'get_basket/$',
        api.get_basket,
        name="get_basket"),
    url(r'basket/$',
        views.BasketView.as_view(),
        name="basket")
]
