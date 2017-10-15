from datetime import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from longclaw.settings import PRODUCT_VARIANT_MODEL
from longclaw.longclawshipping.models import Address

@python_2_unicode_compatible
class Order(models.Model):
    SUBMITTED = 1
    FULFILLED = 2
    CANCELLED = 3
    REFUNDED = 4
    FAILURE = 5
    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                      (FULFILLED, 'Fulfilled'),
                      (CANCELLED, 'Cancelled'),
                      (REFUNDED, 'Refunded'),
                      (FAILURE, 'Payment Failed'))
    payment_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    status_note = models.CharField(max_length=128, blank=True, null=True)

    transaction_id = models.CharField(max_length=256, blank=True, null=True)

    # contact info
    email = models.EmailField(max_length=128, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    # shipping info
    shipping_address = models.ForeignKey(
        Address, blank=True, null=True, related_name="orders_shipping_address")

    # billing info
    billing_address = models.ForeignKey(
        Address, blank=True, null=True, related_name="orders_billing_address")

    shipping_rate = models.DecimalField(max_digits=12,
                                        decimal_places=2,
                                        blank=True,
                                        null=True)

    def __str__(self):
        return "Order #{} - {}".format(self.id, self.email)

    @property
    def total(self):
        """Total cost of the order
        """
        total = 0
        for item in self.items.all():
            total += item.total
        return total

    @property
    def total_items(self):
        """The number of individual items on the order
        """
        return self.items.count()


    def refund(self):
        """Issue a full refund for this order
        """
        from longclaw.utils import GATEWAY
        now = datetime.strftime(datetime.now(), "%b %d %Y %H:%M:%S")
        if GATEWAY.issue_refund(self.transaction_id, self.total):
            self.status = self.REFUNDED
            self.status_note = "Refunded on {}".format(now)
        else:
            self.status_note = "Refund failed on {}".format(now)
        self.save()

    def fulfill(self):
        """Mark this order as being fulfilled
        """
        self.status = self.FULFILLED
        self.save()

    def cancel(self, refund=True):
        """Cancel this order, optionally refunding it
        """
        if refund:
            self.refund()
        self.status = self.CANCELLED
        self.save()

@python_2_unicode_compatible
class OrderItem(models.Model):
    product = models.ForeignKey(PRODUCT_VARIANT_MODEL, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)

    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return "{} x {}".format(self.quantity, self.product.get_product_title())
