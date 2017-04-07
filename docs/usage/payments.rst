.. payments:

Payment Backends
==================

Longclaw supports payment capture through Stripe, Braintree and Paypal (Using the Braintree VZero SDK).

To select the payment gateway to use, you must specify the ``PAYMENT_GATEWAY`` attribute in your ``settings.py``.

The options are:

- ``longclaw.longclawcheckout.gateways.base.BasePayment``. A do-nothing base implementation
- ``longclaw.longclawcheckout.gateways.stripe.StripePayment``. Capture payments using Stripe.
- ``longclaw.longclawcheckout.gateways.braintree.BraintreePayment``. Capture payments using Braintree.
- ``longclaw.longclawcheckout.gateways.braintree.PaypalVZeroPayment``. Capture Paypal payments using the braintree v.zero SDK.


Additional Settings and dependencies
------------------------------------

To use payment gateways it is necessary to specify API keys and install client SDK's for the chosen payment provider.

:Stripe:
  ``STRIPE_PUBLISHABLE`` - Your public api key
  ``STRIPE_SECRET`` - Your secret api key
  You will need to install the stripe python sdk (``pip install stripe``)

:Braintree:
  ``BRAINTREE_MERCHANT_ID`` - Your braintree merchant account ID.
  ``BRAINTREE_PUBLIC_KEY`` - Your public api key
  ``BRAINTREE_PRIVATE_KEY`` - Your secret api key

:Paypal:
  ``VZERO_ACCESS_TOKEN`` - Your access token for the v.zero SDK.

Paypal and braintree require the braintree python SDK (``pip install braintree``)


.. _custom-integrations:

Custom Integrations
===================

To implement your own payment integration, you must implement the payment gateway interface. This is simple:

- Inherit from ``longclaw.longclawcheckout.gateways.base.BasePayment``
- Implement ``create_payment``. This should take a ``request`` object, an ``amount`` and optionally a ``description``. 
  It should use these to capture the payment using your chosen provider. For examples see the implementations in
  ``longclaw.longclawcheckout.gateways``
- Implement the ``get_token`` method. This method should generate tokens used by the payment provider. It accepts a ``request``
  object containing post data (``request.data``). Tokens returned may represent different things depending on the 
  payment provider - e.g. it may be used to tokenize payment details or generate authentication tokens.

You can define your own requirements for the request data to be submitted to the functions.
``create_payment`` is called in a POST request to the ``checkout/`` api. ``get_token`` is similarly called 
in a POST request to the ``checkout/token/`` api.