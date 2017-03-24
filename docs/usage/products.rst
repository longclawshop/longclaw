.. _products:

Adding Products
===============

Your new longclaw project has ``products`` app installed with a ``ProductVariant`` model. 
You should add your own custom fields to ``ProductVariant`` to meet the demands of your catalogue.

A ``ProductVariant`` is a child of the longclaw ``Product`` model and is used to represent variants of a single product.
E.g different sizes, colours etc.

Writing the templates
-----------------------

Since ``ProductIndex`` and ``Product`` are Wagtail pages, HTML templates should be created for each. 
The developer should refer to the `Wagtail documentation <http://docs.wagtail.io/en/v1.8.1/topics/writing_templates.html>`_ for further details.
Basic example templates are provided in ``your_project/templates/longclawproducts/`` when creating a project
with the longclaw project template.


