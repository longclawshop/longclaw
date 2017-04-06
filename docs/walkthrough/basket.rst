.. _walkthrough-basket:

Displaying the Basket
=====================

Longclaw provides a REST API endpoint for retrieving basket data and a django view. 

To use the django view, we must provide a template titled ``longclawbasket/basket.html``. 
It is common to provide a link to the basket page in the header. We can use the ``url`` tag in
our site header to provide the link::

    {% url 'longclaw-basket' %}