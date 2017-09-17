.. _products:

Adding Products
===============

Your new longclaw project has ``products`` app installed with ``ProductVariant``, ``Product`` and ``ProductIndex`` models.
You should add your own custom fields to ``ProductVariant`` to meet the demands of your catalogue.

A ``ProductVariant`` is a child of the ``Product`` model and is used to represent variants of a single product.
E.g different sizes, colours etc.

``Product`` and ``ProductIndex`` are not required by longclaw, although this way of modelling your catalogue means that:

- Your models fit into Wagtail way of creating ``Page`` models. Here, ``Product`` is your ``Page``, with ``ProductVariant`` being an
  inline model. ``ProductIndex`` is the index page for listing all ``Products``.

- It is easy with this setup to model fairly simple catalogues where each product has multiple options. E.g. a music shop selling
  CD and vinyl versions of each product.

Other examples might include having multiple ``ProductIndex`` models to represent different catalogues - e.g. clothing lines
or categories in a large shop.
You may also wish to create of supporting models for images, categories, tags etc. This is all up to you.

Writing the templates
-----------------------

Since ``ProductIndex`` and ``Product`` are Wagtail pages, HTML templates should be created for each.
The developer should refer to the `Wagtail documentation <http://docs.wagtail.io/en/v1.8.1/topics/writing_templates.html>`_ for further details.
Basic example templates are provided in ``your_project/templates/longclawproducts/`` when creating a project
with the longclaw project template.


