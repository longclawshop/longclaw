
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

  (my_project) $ pip install -e git+https://github.com/JamesRamm/longclaw.git#egg=longclaw

We also need to install the client library for our payment gateway integration. We are going to
use Paypal as our payment gateway in this walkthrough. To make things easy, we will use Paypal 
Express Checkout. For this we can use the Braintree SDK:

.. code-block:: bash

  (my_project) $ pip install braintree

As longclaw is not yet released, you will need to build the assets:

.. code-block:: bash

  (my_project) $ longclaw build

Finally, use longclaw to bootstrap your django project:

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
``'longclaw.longclawcheckout.gateways.BasePayment'`` to ``'longclaw.longclawcheckout.gateways.PaypalVZero'``

We also need to set the access token. The setting for this is ``VZERO_ACCESS_TOKEN``. Paypal access tokens
are termed something like ``access_token$sandbox`` followed by a sequence of characters. As we have different
access tokens for sandbox and live accounts, we will set ``VZERO_ACCESS_TOKEN`` in ``my_shop/settings/dev.py``
for the sandbox account and ``my_shop/settings/production.py`` for the live account.

.. note: Don't forget that Longclaw is a Wagtail project. You may need to configure additional settings
  for wagtail.


Great! Now we are setup, we can start :ref:`adding products <tutorial_products>`