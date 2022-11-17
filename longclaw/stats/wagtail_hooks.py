from django.urls import path, reverse
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.menu import MenuItem, SubmenuMenuItem
from wagtail.contrib.modeladmin.menus import (  # TODO: seeing console warnings about this being deprecated v5.0
    SubMenu,
)

from longclaw.stats import views

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks


@hooks.register("register_admin_urls")
def register_longclaw_stats_url():

    return [
        path("longclaw_stats/", views.longclaw_stats_view, name="longclaw_stats"),
    ]


@hooks.register("register_admin_menu_item")
def register_longclaw_stats_menu_item():

    menu_items = [
        MenuItem("Dashboard", reverse("longclaw_stats"), icon_name="table", order=10000)
    ]

    return SubmenuMenuItem(
        "Longclaw", SubMenu(menu_items), icon_name="table", order=10000
    )
