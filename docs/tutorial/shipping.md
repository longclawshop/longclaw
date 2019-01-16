---
title: Configuring Shipping
sidebar_label: Shipping
---

Now we can display products and add them to the basket, we must configure our shipping rates
before setting up the checkout process.


## Per Country Rates


Shipping rates are set on a per-country basis via the `Shipping` page in the wagtail admin. 
Initially, no countries will be available - Longclaw comes with a set of country data which can be loaded into the database
using the `loadcountries` command:

```bash
    python manage.py loadcountries
```

In the image below, we set a standard rate for the UK. It is possible to select multiple countries
for a rate to apply to. We can also create more than one shipping rate for the same country.

![Shipping](assets/shipping.png)

## Default Shipping Rate

We can configure a default shipping rate to apply to all countries we have not explicitly specified. 

> By enabling default shipping, you imply that you ship to *all* countries. If you do not wish this
  you should *not* enable default shipping. 

To enable default shipping:

- Select `settings` from the wagtail admin menu
- Select `Configuration`
- Fill in `Default Shipping Rate` and `Default Shipping Carrier`
- Ensure `Enable Default Shipping` is checked.

![Default shipping](assets/default_shipping.png)

### Currency

You can also define the currency in `Longclaw Settings`. This applies site wide. It is mostly semantic -
Longclaw assumes all calculations & prices are in the same currency - however some payment gateways require the 
currency to be specified.
