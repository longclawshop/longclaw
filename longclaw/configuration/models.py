"""
Admin confiurable settings for longclaw apps
"""
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from django.db import models

from longclaw.shipping.models import Address


@register_setting
class Configuration(BaseSetting):
    default_shipping_rate = models.DecimalField(
        default=3.95,
        max_digits=12,
        decimal_places=2,
        help_text='The default shipping rate for countries which have not been configured'
    )
    default_shipping_carrier = models.CharField(
        default="Royal Mail",
        max_length=32,
        help_text='The default shipping carrier'
    )
    default_shipping_enabled = models.BooleanField(
        default=False,
        help_text=('Whether to enable default shipping.'
                   ' This essentially means you ship to all countries,'
                   ' not only those with configured shipping rates'))
    
    shipping_origin = models.ForeignKey(Address, blank=True, null=True, on_delete=models.PROTECT)

    currency_html_code = models.CharField(
        max_length=12,
        default="&pound;",
        help_text="The HTML code for the currency symbol. Used for display purposes only"
    )
    currency = models.CharField(
        max_length=6,
        default="GBP",
        help_text="The iso currency code to use for payments"
    )

    panels = (
        FieldPanel('default_shipping_rate'),
        FieldPanel('default_shipping_carrier'),
        FieldPanel('default_shipping_enabled'),
        SnippetChooserPanel('shipping_origin'),
        FieldPanel('currency_html_code'),
        FieldPanel('currency')
    )
