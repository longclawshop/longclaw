===============
Longclaw
===============

.. image:: https://badge.fury.io/py/longclaw.svg
    :target: https://badge.fury.io/py/longclaw

.. image:: https://codecov.io/gh/JamesRamm/longclaw/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/JamesRamm/longclaw

.. image:: https://travis-ci.org/JamesRamm/longclaw.svg?branch=master
    :target: https://travis-ci.org/JamesRamm/longclaw

.. image:: https://landscape.io/github/JamesRamm/longclaw/master/landscape.svg?style=flat
   :target: https://landscape.io/github/JamesRamm/longclaw/master
   :alt: Code Health

.. image:: https://readthedocs.org/projects/longclaw/badge/?version=latest
    :target: http://longclaw.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

An e-commerce extension for `Wagtail CMS <https://github.com/wagtail/wagtail>`_

``Longclaw is currently undergoing a major rewrite to bring it up to date with wagtail/django 2 and pack in more features``

Checkout the `demo site <https://github.com/JamesRamm/longclaw_demo>`_ and `documentation <http://longclaw.readthedocs.io/en/latest/>`_

.. image:: docs/_static/images/dashboard.png
    :alt: Longclaw dashboard

Quickstart
----------
Install Longclaw::

  $ pip install longclaw

Setup a Wagtail+Longclaw project::

  $ longclaw start my_project

Features
--------
- Integrated with Wagtail. Order management, shipping rates, product pages etc are all managed from the Wagtail admin, allowing you to fully leaverage the power of Wagtail.
- Multiple payment backends. Longclaw currently supports Stripe, Braintree and PayPal (v.zero) payments.
- Comprehensive REST API & javascript client easily loaded via a template tag
- Create your catalogue as Wagtail pages, with complete control over your product fields
- Easy setup. Just run ``longclaw start my_project`` to get going
- Simple to use, simple to change. Write your frontend as you would any other wagtail website. No complicated overriding, forking etc in order to customise behaviour.


Screenshots
***********
.. image:: docs/_static/images/order_detail.png


Support
--------

Please raise bugs/feature requests using the github issue tracker and ask questions on stackoverflow.
For further support contact ramshacklerecording@gmail.com


