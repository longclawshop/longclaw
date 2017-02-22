.. getting_started

Getting Started
================

Longclaw is an e-commerce solution for Python built using Wagtail CMS and Django.
It is currently in beta and can be installed using pip:

    $ pip install git+git://github.com/JamesRamm/longclaw

Longclaw provides a template to setup a Longclaw/Wagtail project::

    $ django-admin startproject --template /path/to/longclaw/project_template/ --ext py,js,css,html project_name

This will provide you with a minimal Wagtail & longclaw website. 
Longclaw integrates tightly with Wagtail, so you should be familiar with developing Wagtail sites before continuing:
http://docs.wagtail.io/

Next, you will need to model your catalogue.

.. toctree::
    :maxdepth: 2

    products
    shipping
    basket_checkout
    payments
    orders


