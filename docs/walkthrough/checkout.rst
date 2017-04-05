

Checkout with Paypal Express
============================

Longclaw offers integration with a few payment gateways and it is also fairly easy to integrate your own.
For this tutorial, we will use Paypal Express Checkout to process payments.

Settings and Dependencies
-------------------------

The payment gateway to use must be set in the settings file:

.. code-block:: python

    PAYMENT_GATEWAY = 'longclaw.longclawcheckout.gateways.braintree.PaypalVZeroPayment'

The ``PaypalVZeroPayment`` class will allow us to take payments using Paypal Express Checkout and is dependent on the
braintree SDK. 

We will need to install this SDK as it is not an explicit dependency of longclaw::

    pip install braintree

That is all we need to do to configure our backend!

Front end integration
---------------------

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
