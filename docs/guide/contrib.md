---
title: Product Requests
sidebar_label: Product Requests
---

This module allows customers to 'request' products which are otherwise out of stock.
The request date and product variant are stored, with the customer email optionally being stored (The ``ProductRequest`` model
contains a field for this, but template tags by default do not collect this information - it is up to you to store it.)

To install, add it to your ``INSTALLED_APPS`` after other longclaw modules:

.. code-block:: python

    INSTALLED_APPS = (
      ...,
      "longclaw.contrib.productrequests"
    )


To show a 'request' button, you can use the following template tag on your product page:

.. code-block:: django

    {% load productrequests_tags %}

    {% for variant in page.variants.all %}
    {% make_request_btn variant_id=variant.id %}
    {% endfor %}


You can also pass ``btn_class`` and ``btn_text`` to change the CSS class and text of the resulting ``button`` element.
By default they are ``btn btn-default`` and ``Request Product``.

This template tag will take care of making the AJAX call to register a request against the product variant.
In order to collect further information - i.e the customer email, you will need to create the button and necessary javascript
yourself. You can use the API client function ``requestList`` to post the collected data.

You can view all requests in the admin index page for your product collections. When hovering over a product, alongside
the usual `Edit`, `View Live` and `Add Child Page` buttons is a new `View Requests` button. This will take you to a page
showing all requests made for each variant of the product.
