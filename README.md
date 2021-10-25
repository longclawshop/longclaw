# Longclaw


## Call For Maintainers
If you are interested in developing this project, please get in touch
https://github.com/JamesRamm/longclaw/issues/375

[![Pypi Version](https://badge.fury.io/py/longclaw.svg)](https://badge.fury.io/py/longclaw)
[![Codecov Status](https://codecov.io/gh/JamesRamm/longclaw/branch/master/graph/badge.svg)](https://codecov.io/gh/JamesRamm/longclaw)
[![Build Status](https://travis-ci.org/JamesRamm/longclaw.svg?branch=master)](https://travis-ci.org/JamesRamm/longclaw)
[![Code Health](https://landscape.io/github/JamesRamm/longclaw/master/landscape.svg?style=flat)](https://landscape.io/github/JamesRamm/longclaw/master)

An e-commerce extension for [Wagtail CMS](https://github.com/wagtail/wagtail)



Checkout the [documentation](https://jamesramm.github.io/longclaw/)

![Image of the dashboard](docs/assets/dashboard.png)

## Quickstart

Install Longclaw:

```bash
  $ pip install longclaw
```

Setup a Longclaw project

```bash
  $ longclaw start my_project
```

Go to project directory and create missing migrations 

```bash
  $ python manage.py makemigrations home catalog
```

Do migrations for whole project and run 

```bash
  $ python manage.py migrate
  $ python manage.py loadcountries
  $ python manage.py createsuperuser
  $ python manage.py runserver
```

## Features

- Tightly integrated with Wagtail. Create products, manage orders, configure shipping and view statistics all from the Wagtail admin.
- Multiple payment backends. Longclaw currently supports Stripe, Braintree and PayPal (v.zero) payments.
- Comprehensive REST API & javascript client easily loaded via a template tag
- Create your catalogue as Wagtail pages, with complete control over your product fields
- Easy setup. Just run `longclaw start my_project` to get going
- Simple to use, simple to change. Write your frontend as you would any other wagtail website. No complicated overriding, forking etc in order to customise behaviour.


### Screenshots

![Order Detail](docs/assets/order_detail.png)



