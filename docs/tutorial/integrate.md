---
title: Add Longclaw to your existing Wagtail project
sidebar_label: Integrate in your existing project
---

1. Install Longclaw

```bash
  $ pip install longclaw
```

2. Update `INSTALLED_APPS`  in `settings/base.py`

```python
INSTALLED_APPS = [
    # ...
    'longclaw.core',
    'longclaw.configuration',
    'longclaw.shipping',
    'longclaw.products',
    'longclaw.orders',
    'longclaw.checkout',
    'longclaw.basket',
    'longclaw.stats',
    # ...
]
```

3. Add context processor in `TEMPLATES`

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # ...
                'longclaw.configuration.context_processors.currency',
            ],
        },
    },
]
```

4. Add Longclaw to `urls.py`

```python
from longclaw import urls as longclaw_urls

urlpatterns = [
    # ...
    path('', include(longclaw_urls)),
    path('', include(wagtail_urls)),
]
```

5. Create new app

```bash
  $ ./manage.py startapp webshop
```

6. In this new app, add the following models

```
from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from longclaw.products.models import ProductVariantBase, ProductBase

class ProductIndex(Page):
    """Index page for all products
    """
    subpage_types = ('webshop.Product', 'webshop.ProductIndex')


class Product(ProductBase):
    parent_page_types = ['webshop.ProductIndex']
    description = RichTextField()
    content_panels = ProductBase.content_panels + [
        FieldPanel('description'),
        InlinePanel('variants', label='Product variants'),

    ]

    @property
    def first_image(self):
        return self.images.first()


class ProductVariant(ProductVariantBase):
    """Represents a 'variant' of a product
    """
    # You *could* do away with the 'Product' concept entirely - e.g. if you only
    # want to support 1 'variant' per 'product'.
    product = ParentalKey(Product, related_name='variants')

    slug = AutoSlugField(
        separator='',
        populate_from=('product', 'ref'),
        )

    # Enter your custom product variant fields here
    # e.g. colour, size, stock and so on.
    # Remember, ProductVariantBase provides 'price', 'ref' and 'stock' fields
    description = RichTextField()


class ProductImage(Orderable):
    """Example of adding images related to a product model
    """
    product = ParentalKey(Product, related_name='images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]
```
Make sure to update `webshop` to your app name in `subpage_types` and `parent_page_types`.
Also, make sure to add templates for the `ProductIndex` and `Product` pages.
A basic example you can find on [the repo](https://github.com/JamesRamm/longclaw/tree/master/longclaw/project_template/catalog/templates/catalog)

We'll be building on top these basic templates in the next section.

7. Add Longclaw specific settings

```python
PRODUCT_VARIANT_MODEL = 'webshop.ProductVariant'
PAYMENT_GATEWAY = 'longclaw.checkout.gateways.BasePayment'
```
We'll be covering their function in the [setup](/docs/guide/install).