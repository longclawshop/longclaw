from django.conf import settings

DEFAULT_SHIPPING_RATE = getattr(settings, 'DEFAULT_SHIPPING_RATE', 3.95)
DEFAULT_SHIPPING_CARRIER = getattr(settings, 'DEFAULT_SHIPPING_CARRIER', 'Royal Mail')
DEFAULT_SHIPPING_ENABLED = getattr(settings, 'DEFAULT_SHIPPING_ENABLED', True)

PAYMENT_GATEWAY = getattr(settings, 'PAYMENT_GATEWAY', 'checkout.gateways.BraintreePayment')
CURRENCY = getattr(settings, "CURRENCY", "GBP")
