from django.utils.safestring import mark_safe
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from longclaw.shipping.models import ShippingRate


class ShippingRateModelAdmin(ModelAdmin):
    model = ShippingRate
    menu_label = "Shipping"
    menu_order = 200
    menu_icon = "site"
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = (
        "name",
        "rate",
        "carrier",
        "description",
        "shipping_country",
    )  # TODO: Add country field and filtering/searching

    def shipping_country(self, obj):
        countries = " | ".join([country.name for country in obj.countries.all()])
        return mark_safe(countries)

    shipping_country.short_description = "Countries"


modeladmin_register(ShippingRateModelAdmin)
