.. getting_started

Getting Started
================

Longclaw is built using Wagtail CMS so this document assumes you have already setup a wagtail project.
If not, starting a wagtail project is easy and documented `here<http://docs.wagtail.io/en/v1.8.1/getting_started/index.html>`_

With this done, you can install Longclaw::

    $ pip install longclaw

You will need to add a couple of Wagtail contrib modules and dependencies aswell as Longclaws' apps to your `INSTALLED_APPS`::

.. code-block:: python

    'wagtail.contrib.modeladmin',
    'wagtail.contrib.settings',

    'rest_framework',
    'django_extensions',

    'longclaw.longclawsettings',
    'longclaw.shipping',
    'longclaw.products',
    'longclaw.basket',
    'longclaw.checkout',
    'longclaw.orders'

URL Configuration
------------------

Add the longclaw URLs' to your `urls.py`:

.. code-block:: python

    from longclaw.basket import urls as basket_urls
    from longclaw.checkout import urls as checkout_urls
    from longclaw.orders import urls as orders_urls
    from longclaw.shipping import urls as shipping_urls

    urlpatterns = [
      ...
      url(r'^api/', include(basket_urls)),
      url(r'^api/', include(checkout_urls)),
      url(r'^api/', include(orders_urls)),
      url(r'^api/', include(projects_urls)),
      url(r'^api/', include(shipping_urls)),
      ...
    ]

This is in addition to the standard Wagtail URL's.

.. toctree::
    :maxdepth: 2

    products
    shipping
    basket_checkout
    payments
    orders


