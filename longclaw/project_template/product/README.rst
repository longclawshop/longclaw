Demo project template
----------

1. Template Product_index.html

Add it to your `Products models.py`:

.. code-block:: python

    class ProductIndex(Page):
          pass

          def get_context(self, request):
             # Update context to include only published products, ordered by reverse-chron
             context = super(ProductIndex, self).get_context(request)
             product = self.get_children().live().order_by('-first_published_at')
             context['product'] = product
             return context
