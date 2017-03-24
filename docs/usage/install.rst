.. _install:

Installing Longclaw
====================

Longclaw is currently in pre-release development and can be installed from github using pip:

.. code-block:: bash

    $ pip install git+git://github.com/JamesRamm/longclaw

Since there is not yet a release distribution of Longclaw, you will need to build the front end assets yourself. 
The Longclaw CLI provides a command to help with this:

.. code-block:: bash

  $ longclaw build

Building the assets requires Node.js & npm. The first release of Longclaw will bundle the assets. 

.. note: You can also build your own source distribution of longclaw using ``python setup.py sdist``. 
  This will also compile the front end assets. 

The Longclaw CLI can then be used to start a new Wagtail/Longclaw project. It behaves much the same as 
the Wagtail CLI::

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
