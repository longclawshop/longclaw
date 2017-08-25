.. checkout:

Checkout
========

Longclaw provides a simple, single checkout view.
The URL for the checkout is ``'checkout/'``.
After a successful checkout, it is redirected to ``checkout/success/``.

To implement the checkout, simply provide ``'longclawcheckout/checkout.html'`` and
``'longclawcheckout/success.html'`` templates. (Empty templates will have been created if
you ran the longclaw CLI to start your project)

There are three forms provided in the checkout view:

:checkout_form:
  Captures the email address and optionally the shipping option for the checkout.
  Also captures a boolean indicating whether a different billing address should be used

:shipping_form:
  Captures shipping information.

:billing_form:
  A second address form for capturing alternate billing information. If you do not submit this form
  (e.g. by not rendering it on the template), the billing and shipping addresses are assumed to be the same.

Generally, you may need to use a little javascript to optionally render the form if the user selects
'different billing address'.

Shipping Options and Javascript
--------------------------------

The shipping option dropdown has no options by default - this is because it is dependent on the shipping country.
The checkout form includes the necessary javascript to do this - you just need to include it on the page.
You will typically also need to include your chosen payment gateways' client javascript:

..code-block:: django

  {% gateway_client_js as scripts %}
  {% for js in scripts %}
  {{ js|safe }}
  {% endfor %}

  {% longclaw_client_bundle %}
  {{ checkout_form.media }}
  <script type="text/javascript">
  initShippingOption('{% longclaw_api_url_prefix %}');
  </script>

The first half uses the ``gateway_client_js`` template tag to load all the payment gateway javascript. There may be one or more.
The second half has three parts to it:

1. ``{% longclaw_client_bundle %}`` loads the longclaw client API, which is required by the checkout form javascript.
2. ``{{ checkout_form.media }}`` loads the javascript required by the checkout form.
3. The last script initializes the checkout javascript. It requires the longclaw API url prefix (which you can customise in your settings)
  to be passed in - there is a template tag to do this for you. You can also optionally specify the ``shippingCountrySelectId`` and ``shippingOptionSelectId``.
  These are the ID's of the select element. You would only need to pass these in if you are going to change them from the defaults.

After this, when you change the shipping country, the shipping option should change appropriately.

..note:: We will hopefully improve this in future releases - any ideas and PR's are welcome!


Payment forms
-------------

It is up to you to render a payment form and then pass the token in the POST data.
Normally, the payment gateway chosen will have a javascript integration to render a form for you
and tokenize the payment method (e.g. braintrees 'hosted fields')

Longclaws' payment gateways provide some helpful utilities to load client javascript and generate tokens.
Loading ``longclawcheckout_tags`` in your template will allow you to retrieve the gateways' javascript libraries
as script tags (``{% gateway_client_js %}`` and generate a client token (``{% gateway_token %}``).
A little javascript is then required to setup your form and ask the gateway to tokenize the payment method for you.
You should then add this token to the request POST data (e.g. with a hidden input field).

For in-depth info on integration, see the walkthrough.
