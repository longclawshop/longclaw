.. checkout:

The Checkout API
================
The checkout API allows you to create more complex javascript-based checkout flows by providing some
simple endpoints for capturing payments and orders. 
In the front end, you should:

- Collect the customer email
- Collect the shipping and billing address
- Payment capture by tokenizing the payment method (e.g. credit card) or payment itself
- (Optionally) calculate the shipping costs
- Submit all the information to the server in an AJAX POST request. 

The first two are relatively simple to achieve. Longclaw provides some utilities to help with the rest.

Payment Capture
===============
With Longclaw you can either tokenize the customers payment method (e.g. credit card) and 
send this to the server for the payment to be captured, or you can use a service such as paypal
express checkout, which captures the payment directly and returns a token representing the transaction
id. You would then submit this token to your server.

The second option is often easiest to integrate since the user is redirected to the 3rd party site for payment.
(This is increasingly done via a modal popup rather than a redirect, which makes the user experience smoother).
The first option offers tightest integration with the look and feel of your site, but invariable involves more 
front end work and validation. 

Tokenizing the Payment
+++++++++++++++++++++++

To capture the payment with a 3rd party service, you will include some external javascript on your page
and often designate a button or ``div`` to initialise the popup/redirect. You will also specify a submit 
handler to receive the token representing the transaction. 

For example, the braintree javascript client allows express checkout using Paypal. Full details of how 
to setup are `here <https://developers.braintreepayments.com/guides/paypal/checkout-with-paypal/javascript/v3>`_.
Other providers such as Stripe offer similar services. 

Once you have received this token, you should submit it, along with the shipping address, billing address,
email and shipping rate to the ``api/checkout/prepaid/`` endpoint. 


.. note:: The ``api/`` prefix can be configured in your django settings under ``API_URL_PREFIX``. 
          For example, if you want to distinguish the longclaw API from your own, you could set ``API_URL_PREFIX="api/longclaw/"``
          The checkout url would then be ``api/longclaw/checkout/prepaid/``          

The JSON request data would look like:

.. code-block:: json

    {
        transaction_id: "...",
        shipping_rate: 0.0,
        email: "john@smith.com",
        address: { 
          shipping_name: "john smith",
          shipping_address_line_1": "...",
          shipping_address_city: "",
          shipping_address_zip: "",
          shipping_address_country: "",
          billing_name: "john smith",
          billing_address_line_1: "...",
          billing_address_city: "",
          billing_address_zip: "",
          billing_address_country: "",
        }
    }

transaction_id
     The token returned from e.g. paypal

When using this method, you do not need to define the ``PAYMENT_GATEWAY`` setting.

Tokenizing the Payment method
+++++++++++++++++++++++++++++

Alternatively, you can pass the payment method for Longclaw to manually capture the payment.
Longclaw expects the payment details (i.e. credit card) to be passed as some kind of token in 
a POST request to ``api/checkout/``. 
Longclaw will then use the payment gateway defined by the ``PAYMENT_GATEWAY`` setting to capture 
the payment. 
To create the initial token representing the customers payment information, you may be able to use
the ``api/checkout/token/`` endpoint, passing the card information in the request data. This is dependent 
upon the backend and it may be preferable to use client javascript libraries provided by your payment
gateway (e.g. ``stripe.js`` or ``braintree-web`` ) to generate a token. 

Once the token is generated, the request data to send to ``api/checkout/`` is very similar to that for
``api/checkout/prepaid/``:

.. code-block:: json

    {
        token: "...",
        shipping_rate: 0.0,
        email: "john@smith.com",
        address: { 
          shipping_name: "john smith",
          shipping_address_line_1: "...",
          shipping_address_city: "",
          shipping_address_zip: "",
          shipping_address_country: "",
          billing_name: "john smith",
          billing_address_line_1: "...",
          billing_address_city: "",
          billing_address_zip: "",
          billing_address_country: "",
        }
    }

token
  The token for customer details. The key name is dependent on the backend ("token" for stripe, "payment_method_nonce" for braintree)

shipping_rate
  Number or string representation of a number (will be cast to float). The shipping costs

email
  The customers' email 

.. note:: The ``"token"`` key is dependent upon the payment backend and may be named differently.

Both ``api/checkout/`` and ``api/checkout/prepaid/`` return a 201 response with ``order_id`` in the JSON data.
If the payment fails, ``api/checkout/`` will return a 400 response with ``order_id`` and ``message`` in the JSON data.

Calculating Shipping Costs
==========================

You will have noticed the need to send ``shipping_rate`` with the checkout. If you are using Longclaws' shipping 
settings, you can easily calculate the shipping cost either in python or by using the ``api/shipping/cost/`` endpoint.

Python example:

.. code-block:: python

    from longclaw.longclawshipping import utils
    from longclaw.longclawsettings.models import LongclawSettings

    country_code = "GB" # ISO 2-letter country code for a configured shipping rate
    option = "standard" # Name of shipping rate configured through longclaw admin (only used if more than one shipping rate exists for the given country)

    settings = LongclawSettings.for_site(request.site)

    try:
      data = utils.get_shipping_cost(country_code, option, settings)
    except InvalidShippingRate:
      # More than 1 shipping rate for the country exists,
      # but the supplied option doesnt match any
      pass
    except InvalidShippingCountry:
      # A shipping rate for this country does not exist and ``default_shipping_enabled`` 
      # is set to ``False`` in the longclaw admin settings

Javascript example:

.. code-block:: javascript

      fetch(
        "api/shipping/cost/",
        {
          method: "POST",
          headers: {
            Accept: 'application/json, application/json, application/coreapi+json',
            "Content-Type": 'application/json"
          },
          credentials: "include",
          body: JSON.stringify({
            country_code: "GB",
            shipping_rate_name: "standard"
          })
        }
      ).then(response => {...})




