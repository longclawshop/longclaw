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
    list_display = ('country', 'code', 'num_shipping_rates')
    inspect_view_enabled = True

    def flag(self, obj):
        return obj.country.flag

    def code(self, obj):
        return obj.country.alpha3

    def num_shipping_rates(self, obj):
        return obj.shipping_rates.count()

modeladmin_register(ShippingCountryModelAdmin)
