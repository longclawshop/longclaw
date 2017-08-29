from django.apps import apps
from longclaw.settings import PRODUCT_VARIANT_MODEL

ProductVariant = apps.get_model(*PRODUCT_VARIANT_MODEL.split('.'))


def maybe_get_product_model():
    try:
        field = ProductVariant._meta.get_field('product')
        return field.rel.to
    except:
        pass
