.. orders:

Processing Orders
=================

Longclaw provides an orders app, accessible from the Wagtail admin. An order is created
upon a succesful checkout and contains shipping and product details.
Orders can be 'fulfilled' in the wagtail admin by click ``view`` in the order list view then
selecting ``fulfill``.
As of v0.1 all ``fulfill`` does is set a flag on the product model. We plan to introduce automated 
email support from v0.2.
