=============================
Longclaw
=============================

.. image:: https://badge.fury.io/py/longclaw.svg
    :target: https://badge.fury.io/py/longclaw

.. image:: https://travis-ci.org/JamesRamm/longclaw.svg?branch=master
    :target: https://travis-ci.org/JamesRamm/longclaw
    
.. image:: https://readthedocs.org/projects/longclaw/badge/?version=latest
    :target: http://longclaw.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


A shop for `Wagtail CMS <https://github.com/wagtail/wagtail>`_

Quickstart
----------
Install Longclaw::

  $ pip install git+git://github.com/JamesRamm/longclaw

Note: Longclaw v0.1 is currently in development; expect many changes
    
Setup a Wagtail+Longclaw project::

  $ django-admin startproject --template /path/to/longclaw/project_template/ --ext py,js,css,html project_name

Features
--------

* Order admin page for Wagtail
* Variable shipping rates per country, managed from wagtail admin
* Pluggable basket and checkout API, supporting a variety of payment backends
* Designed to be adaptable to the needs of your own product catalogue
* Complete control of your own front end, just like Wagtail. 

Running Tests
-------------

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

