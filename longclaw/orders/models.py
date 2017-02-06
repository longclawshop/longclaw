from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from longclaw.settings import PRODUCT_VARIANT_MODEL

class Address(models.Model):
    name = models.CharField(max_length=64)
    line_1 = models.CharField(max_length=128)
    line_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=32)

    panels = [
        FieldPanel('name'),
        FieldPanel('line_1'),
        FieldPanel('line_2'),
        FieldPanel('city'),
        FieldPanel('postcode'),
        FieldPanel('country')
    ]

    def __str__(self):
        return "{}, {}, {}".format(self.name, self.city, self.country)

class Order(models.Model):
    SUBMITTED = 1
    FULFILLED = 2
    CANCELLED = 3
    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                      (FULFILLED, 'Fulfilled'),
                      (CANCELLED, 'Cancelled'))
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    status_note = models.CharField(max_length=128, blank=True, null=True)

    # contact info
    email = models.EmailField(max_length=128, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    # shipping info
    shipping_address = models.ForeignKey(Address, related_name="orders_shipping_address")

    # billing info
    billing_address = models.ForeignKey(Address, blank=True, related_name="orders_billing_address")

    @property
    def total(self):
        total = 0
        for item in self.items_set.all():
            total += item.total
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(PRODUCT_VARIANT_MODEL, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)

    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return "{} x {}".format(self.quantity, self.product.get_product_title())
