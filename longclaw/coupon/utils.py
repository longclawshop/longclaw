from django.utils import timezone

from decimal import Decimal
import random


def get_random_promo_code(num):
    # code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code_chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ' # Removed: 0, 1, I, O
    code = ''.join([code_chars[random.randint(0, len(code_chars)-1)] for x in range(num)])
    return code

def week_from_now():
    return timezone.now() + timezone.timedelta(days=7)


def discount_percentage(total, percent):
    new_total = total - (total) * (percent / 100)
    amount_saved = total * (percent / 100)
    return new_total, amount_saved

def discount_dollar(total, dollar):
    new_total = total - dollar
    amount_saved = min(total, dollar) # in case the dollar value is larger than the total amount
    return new_total, amount_saved


def discount_total(total, discount=None):
    '''
    Parameters are:
    total - a floating point value
    discount - an instance of the Discount model (or None)

    Returns the new total after the discount has been applied, and
    the amount saved from the discount
    '''
    if not discount:
        return total, 0
    
    total = total
    
    # check what type of discount it is and apply the value appropriately
    if discount.coupon.discount_type == 'percentage':
        # do percentage stuff
        new_total, amount_saved = discount_percentage(total, discount.coupon.discount_value)
    elif discount.coupon.discount_type == 'dollar':
        new_total, amount_saved = discount_dollar(total, discount.coupon.discount_value)
    else:
        # none of the above, so return the original total
        new_total = total
        amount_saved = 0

    # pretty sure the amount should not go below zero, so check for it
    # if new_total < 0:
    # because stripe doesn't accept payments below $0.50, if the discountSubtotal is
    # in that range, just zero it off
    if new_total <= 0.5:
        new_total = Decimal(0)
        amount_saved = total
    
    return new_total, amount_saved