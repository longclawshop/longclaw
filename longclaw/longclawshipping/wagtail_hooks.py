from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from longclaw.longclawshipping.models import ShippingRate, Address


class ShippingRateModelAdmin(ModelAdmin):
    model = ShippingRate
    menu_label = 'Shipping'
    menu_order = 200
    menu_icon = 'site'
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('name', 'rate', 'carrier', 'description')


modeladmin_register(ShippingRateModelAdmin)

class AddressModelAdmin(ModelAdmin):
    model = Address
    menu_label = 'Address'
    menu_order = 220
    menu_icon = 'group'
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('name', 'line_1', 'city', 'country')


modeladmin_register(AddressModelAdmin)
