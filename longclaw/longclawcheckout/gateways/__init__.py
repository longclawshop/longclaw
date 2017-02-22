'''
Gateways module to hold payment processor backend logic
'''
from longclaw.longclawcheckout.gateways.base import BasePayment
from longclaw.longclawcheckout.gateways.braintree_payment import BraintreePayment, PaypalVZeroPayment
from longclaw.longclawcheckout.gateways.stripe_payment import StripePayment
