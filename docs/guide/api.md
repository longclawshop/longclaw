---
title: API Client
sidebar_label: API Client
---

Longclaw comes with a handy API javascript client to simplify making HTTP requests. 

To load the client into your HTML templates, you can use the template tags:

```django

    {% load longclawcore_tags %}

    {% longclaw_vendors_bundle %}
    {% longclaw_client_bundle %}
```

This will render the `<script>` tags necessary to load the javascript. The api client 
will be available as a global object called `longclawclient`.
You can access the methods by calling the request name (e.g. `basketList`) and the desired method::

    longclawclient.basketList.get({ ... })
    longclawclient.basketList.post({ ... })

## API Reference

### orderDetail
  
supports GET methods. Requires an `id` url parameter
  `longclawclient.orderDetail.get({ urlParams: { id: ... } })`

### fulfillOrder
supports POST methods. Requires an `id` url param.
  `longclawclient.fulfillOrder.post({ urlParams: { id: ... } })`

### checkout
supports POST method. requires JSON data.
  `longclawclient.checkout.post({ data: { ... } })`

### checkoutToken
supports GET method.

### basketList
supports GET and POST methods

### basketListCount
supports GET methods

### basketDetailCount
supports GET method. Requires `id` url param.

### basketDetail
supports DEL method. Requires `id` url param.

### shippingCost
supports GET method. requires `country_code` query param
  `longclawclient.shippingCost.get({ queryParams: { country_code: 'gb' } })`

### shippingCountries
supports GET method

### addressList
supports GET and POST methods

### addressDetail
supports GET, PUT, DEL methods

All methods take a `config` object of options which can optionally contain:

| Parameter   | Description
|:-----------:|----------------
| url         | Completely override the URL to use
| prefix      | Use a different prefix or host for calling the endpoint.
| urlParams   | replacement parameters for the endpoint. for example, if the endpoint is specified as `booking/{id}/`, urlParams should be an object containing an `id` key and the string to replace it with, e.g: `{ id: '123' }` would result in the endpoint being modified to `booking/123/`
| queryParams | An object containing key-value pairs which will be mapped to a query string. E.g. `{ first_name: 'John', last_name: 'Smith' }` would result in the endpoint being modified to `booking/123/?first_name=John&last_name=Smith`
| data       | Data object to send with the POST/PUT request. Will be converted to JSON.


It is important to note the `config.prefix` option. You will almost always need to specify this
to match the `API_URL_PREFIX` setting in your django settings. This can be done by including it in
your template view as e.g. a data attribute on a element and then accessing it through the `dataset`
attribute in javascript, e.g:

```javascript
   document.getElementById('my-element').dataset.apiUrlPrefix
```

### Usage with ES6 modules

To use the client with other ES6+ modules, install the client library from npm:

```bash
   npm i longclawclient --save
```
Then import the api library:
```bash
   import api from 'longclawclient'
```