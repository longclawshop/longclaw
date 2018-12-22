from django.apps import apps
from django.utils.module_loading import import_string
from longclaw.settings import PRODUCT_VARIANT_MODEL, PAYMENT_GATEWAY

GATEWAY = import_string(PAYMENT_GATEWAY)()
ProductVariant = apps.get_model(*PRODUCT_VARIANT_MODEL.split('.'))


def maybe_get_product_model():
    try:
        field = ProductVariant._meta.get_field('product')
        return field.related_model
    except:
        pass
