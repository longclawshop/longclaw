from django.db import models
from longclaw.settings import PRODUCT_VARIANT_MODEL

class ProductRequest(models.Model):
    variant = models.ForeignKey(
        PRODUCT_VARIANT_MODEL, related_name='requests', on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Optional email of the customer who made the request"
    )
