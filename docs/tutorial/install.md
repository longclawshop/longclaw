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

We also need to install the client library for our payment gateway integration. We are going to
use Braintree as our payment gateway in this walkthrough.

```bash
(my_project) $ pip install braintree
```

Finally, use the longclaw CLI to setup your django project:

```bash
(my_project) $ longclaw start bakery
```

## Settings

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
The `catalog` folder contains a skeleton model for our product `variants` which we will come to later.

Before proceeding, we need to setup our ``settings`` file, in ``bakery/settings/base.py``.

We need to configure which payment gateway we are using. Change the entry for `PAYMENT_GATEWAY` from
`'longclaw.checkout.gateways.BasePayment'` to `'longclaw.checkout.gateways.braintree.BraintreePayment'`

We also need to set the access tokens for the braintree backend. Add the following settings:

```python
BRAINTREE_SANDBOX = False
BRAINTREE_MERCHANT_ID = os.environ['BRAINTREE_MERCHANT_ID']
BRAINTREE_PUBLIC_KEY = os.environ['BRAINTREE_PUBLIC_KEY']
BRAINTREE_PRIVATE_KEY = os.environ['BRAINTREE_PRIVATE_KEY']
```

For development/testing, you will probably want to set `BRAINTREE_SANDBOX` to `True`. The above settings assume that
you have set environment variables on your OS with the access tokens.

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