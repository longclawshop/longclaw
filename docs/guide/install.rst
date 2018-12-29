.. _install:

Installing Longclaw
====================

Longclaw can be installed from pypi:

.. code-block:: bash

    $ pip install longclaw

The Longclaw CLI can then be used to start a new Wagtail/Longclaw project. It behaves much the same as 
the Wagtail CLI:

.. code-block:: bash

    $ longclaw start my_project

This will provide you with a minimal Wagtail & longclaw website. 
Longclaw integrates tightly with Wagtail, so you should be familiar with developing Wagtail sites before continuing:
http://docs.wagtail.io/

In order to process real payments, you will need to install the client library for your chosen payment backend. 
This will either be:

- Stripe; ``pip install stripe``
- Braintree (for braintree and paypal payments); ``pip install braintree``

For other payment gateways, you will need to :ref:`write your own integration <custom-integrations>`.

Next, read about :ref:`modelling your catalogue and adding products <products>` to your new site
