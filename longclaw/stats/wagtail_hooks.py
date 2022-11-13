from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks


@hooks.register("register_admin_urls")
def register_longclaw_stats_url():
    from django.urls import path

    from longclaw.stats import views

    return [
        path("longclaw_stats/", views.longclaw_stats_view, name="longclaw_stats"),
    ]


@hooks.register("register_admin_menu_item")
def register_longclaw_stats_menu_item():
    from django.urls import reverse
    from wagtail.admin.menu import MenuItem, SubmenuMenuItem
    from wagtail.contrib.modeladmin.menus import SubMenu

    menu_items = [
        MenuItem("Dashboard", reverse("longclaw_stats"), icon_name="table", order=10000)
    ]

    return SubmenuMenuItem(
        "Longclaw", SubMenu(menu_items), icon_name="table", order=10000
    )
