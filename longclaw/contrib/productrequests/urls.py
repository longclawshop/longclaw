from django.urls import path

from longclaw.contrib.productrequests import api, views
from longclaw.settings import API_URL_PREFIX

request_list = api.ProductRequestViewSet.as_view({"get": "list", "post": "create"})

request_detail = api.ProductRequestViewSet.as_view({"get": "retrieve"})

request_variant = api.ProductRequestViewSet.as_view({"get": "requests_for_variant"})

urlpatterns = [
    path(API_URL_PREFIX + "requests/", request_list, name="productrequests_list"),
    path(
        API_URL_PREFIX + "requests/<pk>/", request_detail, name="productrequests_detail"
    ),
    path(
        API_URL_PREFIX + "requests/variant/<variant_id>/",
        request_variant,
        name="productrequests_variant_list",
    ),
    path("requests/product/<pk>/", views.requests_admin, name="productrequests_admin"),
]
