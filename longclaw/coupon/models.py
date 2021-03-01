from django.db import models
from django.utils import timezone

from wagtail.core import blocks
from wagtail.snippets.models import register_snippet
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from longclaw.settings import PRODUCT_VARIANT_MODEL
from longclaw.orders.models import Order
from longclaw.configuration.models import Configuration

from .utils import get_random_promo_code, week_from_now
from .blocks import (
    DiscountPercentageBlock,
    DiscountDollarBlock
)


@register_snippet
class Coupon(models.Model):
    code = models.CharField(max_length=50)

    discount_type_stream_field = StreamField(
        blocks.StreamBlock([
            ('percentage', DiscountPercentageBlock()),
            ('dollar', DiscountDollarBlock()),
        ], min_num=1, max_num=1),
    )

    description = models.TextField(blank=True, null=True, help_text='Short description of the type of discount. e.g. "50% discount"')
    infinite_redemptions = models.BooleanField(default=False, help_text='Whether or not this coupon can be used an infinite amount of times')
    max_redemptions = models.IntegerField(default=1)
    redemptions = models.IntegerField(default=0) # To track how many times this token has been used

    expiry_date = models.DateTimeField(default=week_from_now, help_text='This coupon will no longer work after this date/time')
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('code'),
        StreamFieldPanel('discount_type_stream_field'),
        FieldPanel('description'),
        FieldPanel('expiry_date'),
        FieldPanel('infinite_redemptions'),
        FieldPanel('max_redemptions'),
        # FieldPanel('redemptions'),
    ]

    # This property is only appropriate now because only one discount type is allowed (at a time)
    @property
    def discount_block(self):
        return self.discount_type_stream_field[0]

    @property
    def discount_type(self):
        return self.discount_block.block.name

    @property
    def discount_value(self):
        return float(self.discount_block.value[self.discount_type])
        
    @property
    def depleted(self):
        if self.infinite_redemptions:
            return False
        elif self.max_redemptions > self.redemptions:
            return False
        return True

    def discount_string(self, amount):
        if self.discount_type == 'percentage':
            return f'{amount:.0f}%'
        elif self.discount_type == 'dollar':
            # return f'{Configuration.objects.first().currency_html_code}{amount}' # don't have time to debug properly, just set the '$' for now
            return f'${amount:.2f}'
        return amount

    def __str__(self):
        string = f'{self.code} - {self.discount_type.title()}'
        name = self.discount_type
        value = self.discount_value
        
        if name == 'percentage':
            string += f' - {value}%'
        elif name == 'dollar':
            string += f' - ${float(value):.2f}'

        if self.infinite_redemptions:
            string += f' (Used {self.redemptions} time{"s" if self.redemptions != 1 else ""})'
        else:
            string += f' (Used {self.redemptions}/{self.max_redemptions})'

        return string


@register_snippet
class Discount(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    basket_id = models.CharField(max_length=32)
    order = models.ForeignKey(Order, related_name='discounts', blank=True, null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(default=timezone.now)
    consumed = models.BooleanField(default=False)
    consumed_date = models.DateTimeField(blank=True, null=True)

    def consume(self, order=None):
        if not order:
            # raise some error
            return
        self.order = order
        self.coupon.redemptions += 1
        self.consumed = True
        self.consumed_date = timezone.now()
        self.save()

    def __str__(self):
        string = f'{self.basket_id} - {str(self.coupon)}'
        if self.order:
            string += f' - {str(self.order)}'
        return string

    class Meta:
        ordering = ['created',]
