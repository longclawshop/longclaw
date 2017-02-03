=============================
Longclaw
=============================

.. image:: https://badge.fury.io/py/longclaw.svg
    :target: https://badge.fury.io/py/longclaw

.. image:: https://travis-ci.org/JamesRamm/longclaw.svg?branch=master
    :target: https://travis-ci.org/JamesRamm/longclaw

.. image:: https://codecov.io/gh/JamesRamm/longclaw/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/JamesRamm/longclaw

A shop for `Wagtail CMS<https://github.com/wagtail/wagtail>`_

Quickstart
----------

Install longclaw::

    pip install longclaw

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'longclaw.products',
        'longclaw.orders',
        'longclaw.checkout',
        'longclaw.basket',
        ...
    )

Add longclaw's URL patterns:

.. code-block:: python

from longclaw.basket.urls import urlpatterns as basket_urls
from longclaw.checkout.urls import urlpatterns as checkout_urls

    urlpatterns = [
        ...
        url(r'^/api/', include(basket_urls, namespace='longclaw')),
        url(r'^/api/', include(checkout_urls, namespace='longclaw')),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
