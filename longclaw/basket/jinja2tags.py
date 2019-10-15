import jinja2
from jinja2 import nodes
from jinja2.ext import Extension

from django.template.loader import get_template

from .templatetags.basket_tags import get_basket_items
from .utils import get_basket_items


def add_to_basket_btn(variant_id, btn_class="btn btn-default", btn_text="Add To Basket"):
    """Button to add an item to the basket
    """
    basket_template = get_template('basket/add_to_basket.html')

    return basket_template.render(context={
        'btn_class': btn_class,
        'variant_id': variant_id,
        'btn_text': btn_text
    })


class LongClawBasketExtension(Extension):
    def __init__(self, environment):
        super(LongClawBasketExtension, self).__init__(environment)

        self.environment.globals.update({
            'basket': jinja2.contextfunction(get_basket_items),
            'add_to_basket_btn': add_to_basket_btn,
        })


# Nicer import names
basket = LongClawBasketExtension
