from django.apps import apps
from longclaw.settings import PRODUCT_VARIANT_MODEL

ProductVariant = apps.get_model(*PRODUCT_VARIANT_MODEL.split('.'))
