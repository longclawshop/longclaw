.. _walkthrough-basket:

Displaying the Basket
=====================

Longclaw provides a REST API endpoint for retrieving basket data and a django view. 

To use the django view, we must provide a template titled ``longclawbasket/basket.html``. 
It is common to provide a link to the basket page in the header. We can use the ``url`` tag in
our site header to provide the link::

    {% url 'longclaw-basket' %}

In the basket template, we have access to all basket items under the ``basket`` context::

    {% for item in basket %}
    ...
    {% endfor %}

For the full implementation of the basket template, take a look at the `longclaw demo repository <https://github.com/JamesRamm/longclaw_demo/blob/master/longclaw_demo/templates/longclawbasket/basket.html>`_
