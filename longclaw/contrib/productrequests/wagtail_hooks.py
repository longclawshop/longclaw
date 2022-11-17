from django.urls import reverse
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin import widgets

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks

from longclaw.utils import ProductVariant


@hooks.register("register_page_listing_buttons")
def product_requests_button(page, page_perms, is_parent=False, next_url=None):
    """Renders a 'requests' button on the page index showing the number
    of times the product has been requested.

    Attempts to only show such a button for valid product/variant pages
    """
    # Is this page the 'product' model?
    # It is generally safe to assume either the page will have a 'variants'
    #  member or will be an instance of longclaw.utils.ProductVariant
    if hasattr(page, "variants") or isinstance(page, ProductVariant):
        yield widgets.PageListingButton(
            "View Requests",
            reverse("productrequests_admin", kwargs={"pk": page.id}),
            priority=40,
        )
