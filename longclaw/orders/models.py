from django.db import models
from longclaw.settings import PRODUCT_VARIANT_MODEL
from longclaw.shipping.models import Address

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

    shipping_rate = models.DecimalField(max_digits=12,
                                        decimal_places=2,
                                        blank=True,
                                        null=True)

    @property
    def total(self):
        total = 0
        for item in self.items.all():
            total += item.total
        return total

    @property
    def total_items(self):
        return self.items.count()

class OrderItem(models.Model):
    product = models.ForeignKey(PRODUCT_VARIANT_MODEL, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)

    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return "{} x {}".format(self.quantity, self.product.get_product_title())
