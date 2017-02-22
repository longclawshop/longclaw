.. shipping:


Configuring Shipping
====================

Longclaw allows you to:

- Enable and set a default shipping rate applicable to any country
- Configure multiple shipping rates for individual countries.

The default shipping rate can be enabled and set from the ``settings -> Longclaw Settings`` menu
in the Wagtail admin. 
If the default shipping rate is enabled, it implies that shipping is available to any country. 
When a rate for a given country cannot be found, the default shipping rate will be used.

Shipping rates for individual countries can be configured via the ``Shipping Countries`` menu in the
Wagtail admin.

For each country added, you can configure any number of shipping rates. Each shipping rate states the
name, description, price and carrier (e.g. Royal Mail). 

