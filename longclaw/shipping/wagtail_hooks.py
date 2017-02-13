from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from longclaw.shipping.models import ShippingCountry


class ShippingCountryModelAdmin(ModelAdmin):
    model = ShippingCountry
    menu_order = 200
    menu_icon = 'site'
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('country', 'country_code', 'shipping_rates')

    def flag(self, obj):
        return obj.country.flag

    def country_code(self, obj):
        return obj.country.alpha3

    def shipping_rates(self, obj):
        return ", ".join(str(rate) for rate in obj.shipping_rates.all())

modeladmin_register(ShippingCountryModelAdmin)
