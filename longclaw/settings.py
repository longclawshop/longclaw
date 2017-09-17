'''
Default settings for longclaw apps
'''
from django.conf import settings

# The payment gateway backend to use
# Can be 'longclaw.longclawcheckout.gateways.braintree.BraintreePayment',
# 'longclaw.longclawcheckout.gateways.braintree.PaypalVZeroPayment',
# 'longclaw.longclawcheckout.gateways.stripe.StripePayment' or 'longclaw.longclawcheckout.gateways.BasePayment'
# Or a custom implementation
PAYMENT_GATEWAY = getattr(settings,
                          'PAYMENT_GATEWAY',
                          'longclaw.longclawcheckout.gateways.base.BasePayment')

# The product variant model to use. This allows custom implementations of
# product models.
PRODUCT_VARIANT_MODEL = getattr(
    settings, 'PRODUCT_VARIANT_MODEL', 'longclawproducts.ProductVariantBase')


# Only required if using Stripe as the payment gateway
STRIPE_PUBLISHABLE = getattr(settings, 'STRIPE_PUBLISHABLE', '')
STRIPE_SECRET = getattr(settings, 'STRIPE_SECRET', '')

# Only required if using Braintree as the payment gateway
BRAINTREE_SANDBOX = getattr(settings, 'BRAINTREE_SANDBOX', False)
BRAINTREE_MERCHANT_ID = getattr(settings, 'BRAINTREE_MERCHANT_ID', '')
BRAINTREE_PUBLIC_KEY = getattr(settings, 'BRAINTREE_PUBLIC_KEY', '')
BRAINTREE_PRIVATE_KEY = getattr(settings, 'BRAINTREE_PRIVATE_KEY', '')

# Only required for using paypal as the payment gateway through braintree v.zero
VZERO_ACCESS_TOKEN = getattr(settings, 'VZERO_ACCESS_TOKEN', '')

API_URL_PREFIX = getattr(settings, 'LONGCLAW_API_URL_PREFIX', 'api/')
