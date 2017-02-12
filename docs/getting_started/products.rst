.. products:

Adding Products
===============

Longclaw provides, ``ProductIndex``, ``Product`` and ``ProductVariant`` models. A ``Product`` is a regular Wagtail ``Page`` and
provides a title, description, images and tags for your product. 
A ``Product`` has one or more ``ProductVariant``s, each which has, at a minimum, a price and a reference.

The ``ProductVariant`` model is designed to be easily replaced by your own model to meet your own requirements (e.g. author, colour, size etc...)


Writing the templates
-----------------------

Since ``ProductIndex`` and ``Product`` are Wagtail pages, HTML templates should be created for each. 
The developer should refer to the `Wagtail documentation<http://docs.wagtail.io/en/v1.8.1/topics/writing_templates.html>`_ for further details.
Example templates are provided in the ``project_template`` directory

Providing your own ``ProductVariant`` model
--------------------------------------------

It is possible to define your own ``ProductVariant`` model by subclassing ``ProductVariantBase`` and
defining ``PRODUCT_VARIANT_MODEL`` in your ``settings.py``.

In your ``models.py``::

.. code-block:: python

    from longclaw.products.models import ProductVariantBase

    class MyProductVariant(ProductVariantBase):

        my_custom_field = models....


In your ``settings.py``::

.. code-block:: python

    PRODUCT_VARIANT_MODEL = "my_app.MyProductVariant"

``ProductVariantBase`` provides the relationship to the ``Product`` model and the following fields:

- price (``DecimalField``)
- ref (``CharField``)
- stock (``IntegerField``)

Longclaws' default ``ProductVariant`` model will still be available as a page type in the Wagtail admin explorer, although shouldn't
be used.

