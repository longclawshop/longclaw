from django.conf.urls import url
from longclaw.basket import api

urlpatterns = [
    url(r'add_to_basket/$',
        api.add_to_basket,
        name="add_to_basket"),
    url(r'remove_from_basket/$',
        api.remove_from_basket,
        name="remove_from_basket"),
    url(r'get_item_count/$',
        api.get_item_count,
        name="get_item_count"),
    url(r'basket_total_items/$',
        api.basket_total_items,
        name="basket_total_items"),
    url(r'get_basket/$',
        api.get_basket,
        name="get_basket"),
]