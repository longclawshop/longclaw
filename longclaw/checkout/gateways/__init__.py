'''
Gateways module to hold payment processor backend logic
'''
from checkout.gateways.braintree_payment import BraintreePayment, PaypalVZeroPayment
from checkout.gateways.stripe_payment import StripePayment
