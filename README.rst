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
    
.. image:: https://img.shields.io/badge/IRC-%23longclaw-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=longclaw&uio=d4
    :alt: IRC Chat

An e-commerce extension for `Wagtail CMS <https://github.com/wagtail/wagtail>`_

`Documentation <http://longclaw.readthedocs.io/en/latest/>`_

  .. figure:: docs/_static/images/dashboard.png
     
     Longclaw dashboard

Quickstart
----------
Install Longclaw::

  $ pip install git+git://github.com/JamesRamm/longclaw

Build the front-end assets (requires node.js & npm)::

  $ longclaw build
    
Setup a Wagtail+Longclaw project::

  $ longclaw start my_project

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
    
Support
--------

Please raise bugs/feature requests using the github issue tracker and ask questions on stackoverflow. 

