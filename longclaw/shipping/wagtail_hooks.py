from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)

from longclaw.shipping.models import ShippingCountry

class ShippingCountryModelAdmin(ModelAdmin):
    model = ShippingCountry
    menu_order = 200
    menu_icon = 'site'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('country_name', 'country_code')
    inspect_view_enabled = True

modeladmin_register(ShippingCountryModelAdmin)
