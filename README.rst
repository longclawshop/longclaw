=============================
Longclaw
=============================

.. image:: https://badge.fury.io/py/longclaw.svg
    :target: https://badge.fury.io/py/longclaw

.. image:: https://travis-ci.org/JamesRamm/longclaw.svg?branch=master
    :target: https://travis-ci.org/JamesRamm/longclaw
    
.. image:: https://readthedocs.org/projects/longclaw/badge/?version=latest
    :target: http://longclaw.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


An e-commerce plugin for `Wagtail CMS <https://github.com/wagtail/wagtail>`_

    .. note:: Longclaw is currently in pre-release development. I am working hard to get a stable v0.1.0 release available. It is likely there will be further breaking changes until then. 

`Documentation <http://longclaw.readthedocs.io/en/latest/>`_

  .. figure:: docs/_static/images/dashboard.png
     
     Longclaw dashboard

Quickstart
----------
Install Longclaw::

  $ pip install git+git://github.com/JamesRamm/longclaw

Note: Longclaw v0.1 is currently in development; expect many changes
    
Setup a Wagtail+Longclaw project::

  $ django-admin startproject --template /path/to/longclaw/project_template/ --ext py,js,css,html project_name

Features
--------

View and fulfill orders from the Wagtail admin
+++++++++++++++++++++++++++++++++++++++++++++++

  .. figure:: docs/_static/images/order_list.png
     
     The orders list can be sorted and filtered by status, date or customer

  .. figure:: docs/_static/images/order_detail.png

Variable Shipping Rates
+++++++++++++++++++++++

Manage your shipping destinations and rates from the Wagtail admin.

Pluggable basket and checkout API
++++++++++++++++++++++++++++++++++

Longclaw provides a simple RESTful API for retrieving/updating the shopping basket and for performing a checkout.
Longclaw currently supports Stripe, Braintree and PayPal (v.zero) payments.

Easy project startup and catalogue modelling
++++++++++++++++++++++++++++++++++++++++++++

Longclaw provides a project template to easily setup your Wagtail + Longclaw project. This sets up a basic ``ProductVariant`` model
so you can get started adding your product-specific fields straight away.

Running Tests
-------------

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

