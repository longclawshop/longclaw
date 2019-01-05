---
title: Setup
sidebar_label: Setup
---

Topics covered:

1. Longclaw installation
2. Scaffolding a project
3. Settings
4. Database migration and initial data


Start off by creating a virtual environment for your project:

```bash
  $ cd my_project_folder
  $ virtualenv my_project
  $ source my_project/bin/activate
```
Install Longclaw into it:

```bash
(my_project) $ pip install longclaw
```

Finally, use the longclaw CLI to setup your django project:

```bash
(my_project) $ longclaw start bakery
```

Now we have a django project which looks like this::

```
my_shop/
  home/
  bakery/
  catalog/
  search/
  manage.py
  requirements.txt
```

The `home` and `search` folders are default folders used in Wagtail projects. Users of Wagtail
will be familiar with these.
The `catalog` folder contains a skeleton model for our product _variants_ which we will come to later.

## Settings
The `settings` module contains global configuration for our website, for both development and production.
If you are familiar with Django, you will already know about `settings`. Longclaw introduces 2 extra settings; 
`PAYMENT_GATEWAY` and `PRODUCT_VARIANT_MODEL`.
Note that the `PRODUCT_VARIANT_MODEL` is already pointing to `'catalog.ProductVariant'`

The `PAYMENT_GATEWAY` refers to the 3rd party payment processor we which to use. Longclaw currently supports
Braintree, Paypal and Stripe. In this tutorial we will use Stripe. We need to install the client python library for
our chosen payment gateway:

```bash
(my_project) $ pip install stripe
```

Now, lets specify the payment gateway in the `settings` module. The file we want to edit is in `bakery/settings/base.py`
(remember, `bakery` is the name of the longclaw project, so replace this with your chosen name).

Change the entry for `PAYMENT_GATEWAY` from `'longclaw.checkout.gateways.BasePayment'` to `'longclaw.checkout.gateways.stripe.StripePayment'`

> By dynamically specifying the `PAYMENT_GATEWAY` longclaw can support custom integrations. See [integrations](guide/payments.md) for more info.

To use Stripe we will need to inform longclaw of our access tokens. To do this, add the following setting:

```python
STRIPE_SECRET = 'sk_live_xxx'
```
Where `sk_live_xxx` is your stripe secret key, accessable from the stripe dashboard, under `Developers -> API Keys`.

> When using Stripe, and indeed most other payment gateways, you can usually use a 'test' key so you can develop without creating real payments.
  In Stripe, the test key will begin with `sk_test_`.

Note that if you are storing your website code in a public repository, or otherwise sharing it, you should be careful about specifying 'secrets' in the code.
Instead, use an environment variable:

```python
STRIPE_SECRET = os.environ['STRIPE_SECRET']
```

## Migration

Now we can run the initial migration and create an admin user:

```bash
python manage.py makemigrations catalog home
python manage.py migrate
python manage.py createsuperuser
python manage.py loadcountries
```

> If you have a problem with the initial migration (`python manage.py migrate`) relating to `InvalidBasesError`, try commenting out all longclaw apps
(and your shop apps, `home`, `search` and the project name app), plus the `ROOT_URLCONF` line and run the migrations again. Next, add back the apps and `ROOT_URLCONF` and
run the migrations one more time. If you encounter problems at runtime, such as `OperationalError: no such table`, try running `migrate` again with the `--run-syncdb` option.

Great! Now we are setup, we can start [adding products](/docs/tutorial/products)