from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from longclaw.settings import PRODUCT_VARIANT_MODEL

@python_2_unicode_compatible
class BasketItem(models.Model):
    basket_id = models.CharField(max_length=32)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    variant = models.ForeignKey(PRODUCT_VARIANT_MODEL, unique=False)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return "{}x {}".format(self.quantity, self.variant)

    def total(self):
        return self.quantity * self.variant.price

    def name(self):
        return self.variant.__str__()

    def price(self):
        return self.variant.price

    def increase_quantity(self, quantity=1):
        ''' Increase the quantity of this product in the basket
        '''
        self.quantity += quantity
        self.save()

    def decrease_quantity(self, quantity=1):
        '''
        '''
        self.quantity -= quantity
        if self.quantity <= 0:
            self.delete()
        else:
            self.save()
