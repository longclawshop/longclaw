.. basket:

Basket
======

The basket (or 'shopping cart') is a collection of ``BasketItem`` objects, tied to the django session and as such, expires when the session expires.

Each ``BasketItem`` has a ``basket_id`` allowing items to be grouped together in a 'basket'.

Fetching the basket
===================

The function ``longclaw.longclawbasket.utils.get_basket_items`` will return all ``BasketItem`` for the current
session. This accepts a django ``request`` object and uses ``longclaw.longclawbasket.utils.basket_id`` to 
fetch the underlying ``basket_id`` on which to filter the ``BasketItem`` objects. 

On the front end, you can use the API endpoint  ``<api_prefix>/get_basket/`` or the django view ``basket/``. You should
provide a template for the view title ``basket.html``. ``basket`` is also the name of the context variable 
containing all basket items.

A ``BasketItem`` has two fields of importance; ``quantity`` and ``variant``. The latter is a foreign key to the 
``ProductVariant`` model. 
In a django template, you can iterate over the basket items like so:

.. code-block:: django

    {% for item in basket %}
       {{ item.quantity }}
       {{ item.variant.price }}
       {{ item.variant.stock }}
       {{ item.variant.ref }}
       {{ item.variant.product.title }}
       {{ item.variant.product.description }}
    {% endfor %}

The API JSON response will contain all fields of the ``ProductVariant`` and ``Product``:

.. code-block:: json

    {
      quantity,
      variant { 
          price,
          stock,
          ref,
          product {
          title,
          description,
          images,
          ...
          }
      }
    }


Adding and Removing items
==========================

Items can be added or removed via the RESTful api:

``<api_prefix>/add_to_basket/`` to add an item and ``<api_prefix>/remove_from_basket/`` to remove an item

For both endpoints, you should provide the product variant id as ``variant_id`` and the ``quantity`` in 
the request data.

There is currently no django view for addition/deletion of basket items. 

Other API endpoints:

``<api_prefix>/get_item_count/``
  get the quantity of a single item in the basket. Requires ``variant_id`` in the request data

``<api_prefix>/basket_total_items/``
  get total number of items in the basket

All basket items can be deleted using the ``longclaw.longclawbasket.utils.destroy_basket`` function.
When an order is successfully placed, the basket will be automatically destroyed.

.. note:: Longclaw does not automatically clean up abandoned baskets. This can occur when a session ends 
          with items still in the basket (i.e the customer did not place an order). This allows you to provide checkout recovery,
          with the caveat that you will need to do your own cleanup of rogue ``BasketItem`` objects when required.
