.. checkout-walkthrough:

Checkout with Braintree
============================

Longclaw offers integration with a few payment gateways and it is also fairly easy to integrate your own.
For this tutorial, we will use Braintree to process payments.

Settings and Dependencies
-------------------------

The payment gateway to use must be set in the settings file:

.. code-block:: python

    PAYMENT_GATEWAY = 'longclaw.longclawcheckout.gateways.braintree.BraintreePayment'


We also need to define settings for access tokens;

.. code-block:: python

    BRAINTREE_SANDBOX = False
    BRAINTREE_MERCHANT_ID = os.environ['BRAINTREE_MERCHANT_ID']
    BRAINTREE_PUBLIC_KEY = os.environ['BRAINTREE_PUBLIC_KEY']
    BRAINTREE_PRIVATE_KEY = os.environ['BRAINTREE_PRIVATE_KEY']

We will need to install this SDK as it is not an explicit dependency of longclaw::

    pip install braintree

That is all we need to do to configure our backend!

Front end integration
---------------------

We will first show how to setup a checkout page using the Checkout view provided by longclaw.
The code shown here is very similar to the implementation of the checkout page here: `Ramshackle Audio<https://github.com/JamesRamm/ramshacklerecording>`_

First, we should load some templatetags which will help us:

.. code-block:: django

  {% load longclawcheckout_tags longclawcore_tags %}

As an aside - you may wish to display the items in the basket on our checkout page. The basket items queryset is available as ``basket``
in the views' context.

Next, we need to setup the forms to gather customer information. There are 2 forms in the context. We will
display and submit them as a single form. Here is an example layout:

.. code-block:: django

    <form action="." method="post" id="checkout-form">
    {% csrf_token %}
    {% for field in shipping_form %}
        {% if field.is_hidden %}
        {{ field }}
        {% else %}
        {% if field.errors %}
        <div class="field error">
        {% else %}
        <div class="field">
        {% endif %}
            <label>{{ field.label_tag }}</label>
            {{ field }}
            {% if field.help_text %}
                <p class="help">{{ field.help_text|safe }}</p>
            {% endif %}
            <div class="ui error message">
                <p>{{ field.errors }}</p>
            </div>
        </div>
        {% endif %}
    {% endfor %}
    {% for field in checkout_form %}
    <!-- purposefully ignoring different billing address option to simplify -->
    {% if field.name == 'different_billing_address' %}
    {% else %}
    {% if field.errors %}
    <div class="field error">
    {% else %}
    <div class="field">
    {% endif %}
        <label>{{ field.label_tag }}</label>
        {{ field }}
        <div class="ui error message">
            {% for error in field.errors %}
            <p>{{ error }}</p>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    {% endfor %}

You may wish to layout the form differently. We have purposefully ignored the ``different_billing_address`` field
since the Braintree dropin-ui will collect a billing postcode anyway, for its' own security checks.

Before we close our `<form>` element, there are 3 further items to add:

.. code-block:: django

      <!-- hidden field for submitting the token back to the server. Name will vary depending on integration-->
      <input type="hidden" id="payment_method_nonce" name="payment_method_nonce"></input>
      <h4 class="ui dividing header">Payment Details</h4>
      <div id="dropin-container"></div>
      <input type="submit" id="submit-button" value="Place Order" class="ui button submit" />
    </form>

We add a hidden field. This field will contain a token (string of characters) given by braintree which represents the payment method.
Most payment gateways require something like this, although the name of the field will change between backends.

We then add an empty div with the id ``dropin-container``. This will contain the Braintree Dropin UI.
We could manually create the fields (using e.g. Hosted Fields for braintree or Elements for stripe) for payment forms, however
most integrations offer some sort of 'dropin' which are increasingly customisable. For most purposes, this will suffice.

Finally, we add a submit button.

The Javascript
***************

OK, so now we have hidden elements, empty containers....we need to get this stuff populated!
Each payment gateway integration provides the necessary javascript libraries to interact with the gateway.
They are made available via a template tag.
Add them like this:

.. code-block:: django

    <!--Load any client javascript provided by the payment gateway.
    I have chosen braintree as my gateway so the template tag below
    should give me a list of script tags which load the braintree
    SDK's
    -->
    {% gateway_client_js as scripts %}
    {% for js in scripts %}
        {{ js|safe }}
    {% endfor %}

    <!--Finally add the media from the checkout form.-->
    {{ checkout_form.media }}

The checkout form also provides a little javascript to initialise shipping options (when the user selects a shipping country).

Finally, we need to add a little of our own javascript to create the braintree dropin:

.. code-block:: django

    <script type="text/javascript">

        //Initialize shipping options - this function is from the
        //checkout form media.
        initShippingOption('{% longclaw_api_url_prefix %}');

        // Initialize the braintree dropin.
        // The gateway token below is taken from the template tag provided by
        // longclaw. This is calculated depending on the chosen
        // PAYMENT_GATEWAY in the user settings.py
        var button = document.querySelector('#submit-button');

        braintree.dropin.create({
            authorization: "{% gateway_token %}",
            container: '#dropin-container'
        }, function (createErr, instance) {
            button.addEventListener('click', function (event) {
            event.preventDefault();
            if (instance){
                instance.requestPaymentMethod(function (err, payload) {
                    // Submit payload.nonce to your server
                    if (err) {
                        // TODO: Handle this error
                        console.log(err);
                    }
                    else {
                        $('#payment_method_nonce').val(payload.nonce);
                        document.getElementById("checkout-form").submit();
                    }
                });
            }
            });
        });
    </script>

Two things are happening in the above code. First, we initialise the shipping options. Note we are using a template tag
to pass the longclaw API url prefix, since this is customisable in your settings.py

Secondly, we initialise the braintree dropin. Again, we use a template tag to get a token for the gateway.
All payment backends provide the ``gateway_token`` template tag, although it is not always necessary.

You may wish to only show the braintree payment form if the user has anything in their basket. In which case you might qualify
the above javascript with ``{% if basket.count > 0 %}`` in your template.

As you can see, setting up the checkout is one of the most involved aspects of creating your store. We have worked to simplify this
for v0.2, but welcome any suggestions on how to make it easier!

If you wish to forego the templatetags & forms (e.g. if making a fully React-based frontend), read on. Otherwise, that is the end of the tutorial!


Javascript-Only integration
----------------------------

Below is a walkthrough of integrating a payment gateway (PayPal) without the aid of templatetags etc..

There is a fair amount of work to do to setup the front end when using any payment gateway. Paypal
Express minimises this for us by taking charge of collecting and tokenizing payment data, although we
must still configure it.

The basic client payment flow with Braintree is as follows:

1. The client requests a braintree token. Longclaw provides an API endpoint to generate tokens using the braintree SDK
2. The client gathers payment details and turns this into a `payment method nonce` by interacting with the braintree server.
    Paypal Express Checkout will take care of this entirely.
3. The client submits the `payment method nonce` to the server to capture the payment. Longclaw provides an API endpoint for all payment captures.

We therefore have three things we need to do in our client-side javascript:

1. Call the longclaw API to generate a token

.. code-block:: javascript

    $.get({
    url: 'api/checkout/token/',
    success: function(response){
      ...
    }
    })

2. Following this, configure the paypal express checkout functionality. This actually has two steps.
  We must first create a braintree `client` using our new token. We then use this to create a braintree
  `paypal` instance.

.. code-block:: javascript

    braintree.client.create({
            authorization: token
        }, (err, client) => {
            if (err) {
              console.log("handle error creating client");
              return;
            };
            braintree.paypal.create({
                client: client
            }, (err, paypalInstance) => {
                if (err) {
                  console.log("handle error creating paypal");
                  return;
                }
                console.log("Paypal instance": paypalInstance);
            });
        });

3. Once paypal has created the `nonce` for the entered payment details, we must submit this
  to our server so longclaw can capture the payment.
  To do this, we must have a button which we want to use to launch the paypal express checkout window.
  We 'attach' the paypal instance we just created to the button like so:

.. code-block:: javascript

    paypalButton.addEventListener(
      'click',
      function (){
          paypalInstance.tokenize({
              flow: 'checkout',
              intent: 'sale',
              amount: totalAmount,
              currency: currency,
              displayName: 'Ramshackle Audio',
              enableShippingAddress: enableShippingAddress,
              shippingAddressEditable: shippingAddressEditable
          }, (err, tokenPayload) => {
              if (!err) {
                  handleSubmit(tokenPayload);
              }
              else {
                  console.log(err)
              }
          });
      });

In this example `paypalButton` is a DOM node referring to the button element we wish to attach paypal to and ``handleSubmit``
is a function which will actually POST the payload to the longclaw api endpoint (``api/checkout/``)

We can make all these nested API calls simpler if we use ES6 Promises and the fetch API:

.. code-block:: javascript

    // Wrap braintree js functions as promises
    function braintreeClientCreate(token){
        return new Promise(function(resolve, reject){
            braintree.client.create({
                authorization: token
            }, (err, data) => {
                if (err) return reject(err);
                resolve(data);
            });
        });
    }

    function braintreePaypalCreate(client){
        return new Promise(function(resolve, reject){
            braintree.paypal.create({
                client: client
            }, (err, data) => {
                if (err) return reject(err);
                resolve(data);
            });
        });
    }

    // functions for tokenizing and calling the longclaw checkout
    function getToken() {
      return fetch(
        '/api/checkout/token/',
        {
          method: 'GET',
          headers: getRequestHeaders(),
          credentials: 'include'    }
      )
        .then(checkStatus)
        .then(parseJSON);
    }

    function checkout(data) {
      return fetch(
        '/api/checkout/',
        {
          method: 'POST',
          headers: getRequestHeaders(isForm),
          credentials: 'include',
          body: JSON.stringify(data)
        }
      )
        .then(checkStatus)
        .then(parseJSON);
    }

    // This is where we actually setup paypal
    export function setupBraintreePaypal(totalAmount,
                                        paypalButton,
                                        shippingAddress,
                                        shippingRate,
                                        email,
                                        currency='GBP',
                                        enableShippingAddress=false,
                                        shippingAddressEditable=false){

      return getToken()
          .then(data => braintreeClientCreate(data.token))
          .then(client => braintreePaypalCreate(client))
          .then(paypalInstance => paypalButton.addEventListener('click',
              function (){
                  paypalInstance.tokenize({
                      flow: 'checkout',
                      intent: 'sale',
                      amount: totalAmount,
                      currency: currency,
                      displayName: 'Ramshackle Audio',
                      enableShippingAddress: enableShippingAddress,
                      shippingAddressEditable: shippingAddressEditable
                  }, (err, tokenPayload) => {
                      if (!err) {
                          return checkout({
                            address: shippingAddress
                            shipping_rate: shippingRate,
                            email: email,
                            payment_method_nonce: tokenPayload.nonce
                          });
                      }
                      else {
                          console.log(err)
                      }
                  });
              })
          )
        }
    }

    // helper functions for making requests
    function getRequestHeaders(form = false) {
      let contentType = 'application/json';
      const headers = {
        Accept: 'application/json, application/json, application/coreapi+json',

      };
      if (!form) headers['Content-Type'] = contentType;
      const csrf = JsCookie.get('csrftoken');
      if (csrf) headers['X-CSRFToken'] = csrf;
      return headers;
    }

    /**
    * Check the response status and raise an error if it's no good.
    * @param {object} response - the http response object as provided by fetch
    * @returns {object} - the http rsponse object or throws an error
    */
    function checkStatus(response) {
      if (response.ok) {
        return response;
      }
      return response.json().then(json => {
        const error = new Error(response.statusText)
        throw Object.assign(error, { response, json })
      })
    }

    /**
    * Return an object given an http json response
    * @param {object} response - json encoded response object as provided by fetch
    * @returns {object} - The parsed json
    */
    function parseJSON(response) {
      return response.json();
    }

The total amount, shipping address, shipping rate and email address of the customer are passed into the setup function;
it is up to the front end developer to create the necessary forms to gather these.
