
Optional Apps
===============

Longclaw comes with a couple of optional apps which can enhance your store.


Product Requests
-----------------

This module allows customers to 'request' products which are otherwise out of stock.
The request date and variant is stored, with the customer email optionally being stored (The ``ProductRequest`` model
contains a field for this, but template tags by default do not collect this information - it is up to you to store it.)

To install, add it to your ``INSTALLED_APPS`` after other longclaw modules:

.. code-block:: python

    INSTALLED_APPS = (
      ...,
      "longclaw.contrib.productrequests"
    )

