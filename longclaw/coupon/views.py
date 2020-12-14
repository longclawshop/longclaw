from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from longclaw.coupon.models import Coupon, Discount
from longclaw.basket.utils import get_basket_items, basket_id
from longclaw.coupon.utils import discount_total
from longclaw.shipping.models.rates import ShippingRate

def verify_discount_code(request):

    # check that we got the 'code' from the request
    if code := request.POST.get('code'):

        # check if the discount code exists
        try:
            coupon = Coupon.objects.get(code=code)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'code': 'DOES_NOT_EXIST',
                'reason': 'There is no existing match for the submitted code',
            })
        else:

            # check if the coupon has expired
            if coupon.expiry_date < timezone.now() and not coupon.infinite_redemptions:
                return JsonResponse({
                    'success': False, 
                    'code': 'EXPIRED', 
                    'reason': 'This discount code has past its expiry date',
                    'coupon': {
                        'type': coupon.discount_type,
                        'value': coupon.discount_value,
                        'description': coupon.description,
                        'expiry_date': coupon.expiry_date,
                    }
                })
            
            # check if the coupons amount of times the coupon has been redeemed exceeds
            # the max amount of times it can be redeemed
            if coupon.depleted:
                return JsonResponse({
                    'success': False,
                    'code': 'DEPLETED',
                    'reason': 'This discount code has no more uses available',
                    'coupon': {
                        'type': coupon.discount_type,
                        'value': coupon.discount_value,
                        'description': coupon.description,
                        'max_redemptions': coupon.max_redemptions,
                        'redemptions': coupon.redemptions,
                        'expiry_date': coupon.expiry_date,
                    }
                })
            

            items, bid = get_basket_items(request)

            # check if the current basket id already has a discount associated with it
            # get (or create) the Discount object 
            # is the object that tracks the transaction of actually using the code form the coupon
            # the order will be attached later when the order is completed
            try:
                discount = Discount.objects.get(
                    basket_id=bid,
                    # coupon=coupon,
                    order=None,
                )
                discount.coupon = coupon
                discount.save()
            except Discount.DoesNotExist:
                discount = Discount(
                    basket_id=bid,
                    coupon=coupon,
                    order=None,
                )
                discount.save()

            # get the total price from the items in the basket and run them through the discount
            total_price = sum(item.total() for item in items)

            if shipping_rate_id := request.POST.get('shipping'):
                try:
                    shipping_rate = ShippingRate.objects.get(id=shipping_rate_id)
                except ShippingRate.DoesNotExist:
                    # don't worry that it doesn't exist, just move along
                    print('couldn\'t find a shipping rate')
                    pass
                else:
                    total_price += shipping_rate.rate

            discount_total_price, discount_total_saved = discount_total(total_price, discount)
            
        
            return JsonResponse({
                'success': True,
                'code': 'VALID',
                'reason': 'This discount code is valid',
                'coupon': {
                    'type': coupon.discount_type,
                    'value': coupon.discount_value,
                    'description': coupon.description,
                    'max_redemptions': coupon.max_redemptions,
                    'redemptions': coupon.redemptions,
                    'expiry_date': coupon.expiry_date,
                    'discount_total_price': discount_total_price,
                    'discount_total_saved': discount_total_saved,
                }
            })

    else:
        return JsonResponse({
            'success': False,
            'code': 'MISSING_CODE',
            'reason': 'No "code" parameter provided',
        })


def remove_basket_discount(request):
    bid = basket_id(request)
    try:
        discount = Discount.objects.get(basket_id=bid, order=None)
        discount.delete()
        return JsonResponse({
            'success': True,
            'code': 'DELETED',
            'reason': 'Removed the discount associated with this basket',
        })
    except Discount.DoesNotExist:
        # this is fine, nothing to delete then
        pass
        return JsonResponse({
            'success': True,
            'code': 'NO_DISCOUNT',
            'reason': 'No discount associated with this basket currently exists',
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'code': 'UNEXPECTED_ERROR',
            'reason': 'Some other unexpected error occured: ' + e,
        })
