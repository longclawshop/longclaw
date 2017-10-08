from django.shortcuts import render
from django.views.decorators.http import require_GET
from wagtail.wagtailcore.models import Page
from longclaw.utils import ProductVariant
from longclaw.contrib.productrequests.models import ProductRequest

@require_GET
def requests_admin(request, pk):
    """Table display of each request for a given product.

    Allows the given Page pk to refer to a direct parent of
    the ProductVariant model or be the ProductVariant model itself.
    This allows for the standard longclaw product modelling philosophy where
    ProductVariant refers to the actual product (in the case where there is
    only 1 variant) or to be variants of the product page.
    """
    page = Page.objects.get(pk=pk).specific
    if hasattr(page, 'variants'):
        requests = ProductRequest.objects.filter(
            variant__in=page.variants.all()
        )
    else:
        requests = ProductRequest.objects.filter(variant=page)
    return render(
        request,
        "productrequests/requests_admin.html",
        {'page': page, 'requests': requests}
    )
