'''
Default settings for longclaw apps
'''
from django.conf import settings

# The payment gateway backend to use
# Can be 'longclaw.longclawcheckout.gateways.BraintreePayment',
# 'longclaw.longclawcheckout.gateways.PaypalVZeroPayment',
# 'longclaw.longclawcheckout.gateways.StripePayment' or 'longclaw.longclawcheckout.gateways.BasePayment'
# Or a custom implementation
PAYMENT_GATEWAY = getattr(settings,
                          'PAYMENT_GATEWAY',
                          'longclaw.longclawcheckout.gateways.BasePayment')

# The product variant model to use. This allows custom implementations of
# product models.
PRODUCT_VARIANT_MODEL = getattr(
    settings, 'PRODUCT_VARIANT_MODEL', 'longclawproducts.ProductVariant')


# Only required if using Stripe as the payment gateway
STRIPE_PUBLISHABLE = getattr(settings, 'STRIPE_PUBLISHABLE', '')
STRIPE_SECRET = getattr(settings, 'STRIPE_SECRET', '')

# Only required if using Braintree as the payment gateway
BRAINTREE_MERCHANT_ID = getattr(settings, 'BRAINTREE_MERCHANT_ID', '')
BRAINTREE_PUBLIC_KEY = getattr(settings, 'BRAINTREE_PUBLIC_KEY', '')
BRAINTREE_PRIVATE_KEY = getattr(settings, 'BRAINTREE_PRIVATE_KEY', '')

# Only required for using paypal as the payment gateway
VZERO_ACCESS_TOKEN = getattr(settings, 'VZERO_ACCESS_TOKEN', '')
