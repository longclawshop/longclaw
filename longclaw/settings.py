'''
Default settings for longclaw apps
'''
from django.conf import settings

# The currency to use for payments
CURRENCY = getattr(settings, "CURRENCY", "GBP")

# Default shipping rate to use when no configured ShippingCountry is found
# for a given address
DEFAULT_SHIPPING_RATE = getattr(settings, 'DEFAULT_SHIPPING_RATE', 3.95)

# Default carrier to use for the default rate
DEFAULT_SHIPPING_CARRIER = getattr(
    settings, 'DEFAULT_SHIPPING_CARRIER', 'Royal Mail')

# Whether to fall back to using the default shipping rate if no ShippingCountry is found
# This means shipping worldwide
DEFAULT_SHIPPING_ENABLED = getattr(settings, 'DEFAULT_SHIPPING_ENABLED', True)

# The payment gateway backend to use
# Can be 'longclaw.checkout.gateways.BraintreePayment',
# 'longclaw.checkout.gateways.PaypalVZeroPayment',
# 'longclaw.checkout.gateways.StripePayment' or 'longclaw.checkout.gateways.BasePayment'
# Or a custom implementation
PAYMENT_GATEWAY = getattr(settings,
                          'PAYMENT_GATEWAY',
                          'longclaw.checkout.gateways.BasePayment')

# The product variant model to use. This allows custom implementations of
# product models.
PRODUCT_VARIANT_MODEL = getattr(
    settings, 'PRODUCT_VARIANT_MODEL', 'products.ProductVariant')


# Only required if using Stripe as the payment gateway
STRIPE_PUBLISHABLE = getattr(settings, 'STRIPE_PUBLISHABLE', '')
STRIPE_SECRET = getattr(settings, 'STRIPE_SECRET', '')

# Only required if using Braintree as the payment gateway
BRAINTREE_MERCHANT_ID = getattr(settings, 'BRAINTREE_MERCHANT_ID', '')
BRAINTREE_PUBLIC_KEY = getattr(settings, 'BRAINTREE_PUBLIC_KEY', '')
BRAINTREE_PRIVATE_KEY = getattr(settings, 'BRAINTREE_PRIVATE_KEY', '')

# Only required for using paypal as the payment gateway
VZERO_ACCESS_TOKEN = getattr(settings, 'VZERO_ACCESS_TOKEN', '')
