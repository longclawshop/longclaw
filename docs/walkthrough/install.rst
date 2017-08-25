
Setting Up
==========

Installation
------------

Start off by creating a virtual environment for your project:

.. code-block:: bash

  $ cd my_project_folder
  $ virtualenv my_project
  $ source my_project/bin/activate

Install Longclaw into it:

.. code-block:: bash

  (my_project) $ pip install longclaw

We also need to install the client library for our payment gateway integration. We are going to
use Braintree as our payment gateway in this walkthrough.

.. code-block:: bash

  (my_project) $ pip install braintree

Finally, use the longclaw CLI to setup your django project:

.. code-block:: bash

 (my_project) $ longclaw start my_shop


Settings
--------

Now we have a django project which looks like this::

   my_shop/
     home/
     my_shop/
     products/
     search/
     manage.py
     requirements.txt

The ``home`` and ``search`` folders are default folders used in Wagtail projects. Users of Wagtail
will be familiar with these.
The ``products`` folder contains a skeleton model for our product `variants` which we will come to later.

Before proceeding, we need to setup our ``settings`` file, in ``my_shop/settings/base.py``.

We need to configure which payment gateway we are using. Change the entry for ``PAYMENT_GATEWAY`` from
``'longclaw.longclawcheckout.gateways.BasePayment'`` to ``'longclaw.longclawcheckout.gateways.braintree.BraintreePayment'``

We also need to set the access tokens for the braintree backend. Add the following settings:

.. codeblock:: python

  BRAINTREE_SANDBOX = False
  BRAINTREE_MERCHANT_ID = os.environ['BRAINTREE_MERCHANT_ID']
  BRAINTREE_PUBLIC_KEY = os.environ['BRAINTREE_PUBLIC_KEY']
  BRAINTREE_PRIVATE_KEY = os.environ['BRAINTREE_PRIVATE_KEY']

For development/testing, you will probably want to set ``BRAINTREE_SANDBOX`` to ``True``. The above settings assume that
you have set environment variables on your OS with the access tokens.

.. note: Don't forget that Longclaw is a Wagtail project. You may need to configure additional settings
  for wagtail.


Great! Now we are setup, we can start :ref:`adding products <tutorial_products>`