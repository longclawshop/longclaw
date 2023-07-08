# Longclaw

## Call For Maintainers

If you are interested in developing this project, please get in touch
https://github.com/JamesRamm/longclaw/issues/375

[![Pypi Version](https://badge.fury.io/py/longclaw.svg)](https://badge.fury.io/py/longclaw)
[![Codecov Status](https://codecov.io/gh/JamesRamm/longclaw/branch/master/graph/badge.svg)](https://codecov.io/gh/JamesRamm/longclaw)
[![Build Status](https://travis-ci.org/JamesRamm/longclaw.svg?branch=master)](https://travis-ci.org/JamesRamm/longclaw)
[![Code Health](https://landscape.io/github/JamesRamm/longclaw/master/landscape.svg?style=flat)](https://landscape.io/github/JamesRamm/longclaw/master)

An e-commerce extension for [Wagtail CMS](https://github.com/wagtail/wagtail)

Checkout the [documentation](https://longclawshop.github.io/longclaw/)

![Image of the dashboard](docs/assets/dashboard.png)

## Project Status

We are working to upgrade the package for the latest versions of Django and Wagtail. While doing this we may need to change the way the package is structured as well as making breaking changes to the code. If you want to use Longclaw in a project, please use the latest release (1.0.2) until we have finished the upgrade.

### Currently supported versions

We are currently running the tests against the following versions of Python, Django and Wagtail.

- Django >= 2.2, < 3.1
- Wagtail >= 2.11, < 2.14
- Python >= 3.7, < 3.10

### Developers

If you are interested in working on this project, please use the [Development setup](#development-setup) instructions below to get started.

## Quickstart

Install Longclaw:

```bash
pip install longclaw
```

Setup a Longclaw project

```bash
longclaw start my_project
```

Go to project directory and create missing migrations 

```bash
python manage.py makemigrations home catalog
```

Do migrations for whole project and run 

```bash
python manage.py migrate
python manage.py loadcountries
python manage.py createsuperuser
python manage.py runserver
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

## Development setup

### Work in progress

The following instructions are for setting up a development environment for Longclaw while we work on the upgrade. If you want to use Longclaw in a project, please use the latest release (1.0.2) until we have finished the upgrade.

#### Create a virtualenv and install the requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[testing]"
```

#### Install and build the frontend

The frontend is built using node and webpack. The version of node required is v12 (LTS). We recommend using [nvm](https://github.com/nvm-sh/nvm) to manage node versions.

```bash
cd longclaw/client
```

Optional: If you are using nvm, you can run `nvm use` to set the correct version of node.

Install the dependencies and build the frontend

```bash
npm install --no-save
npm run build
```

#### Run the tests

```bash
make test
```

#### Run the tests with TOX

```bash
make test-all
```
