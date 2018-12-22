from django import template
from longclaw.basket.utils import get_basket_items

register = template.Library()

@register.simple_tag(takes_context=True)
def basket(context):
    """
    Return the BasketItems in the current basket
    """
    items, _ = get_basket_items(context["request"])
    return items


@register.inclusion_tag('basket/add_to_basket.html')
def add_to_basket_btn(variant_id, btn_class="btn btn-default", btn_text="Add To Basket"):
    """Button to add an item to the basket
    """
    return {
        'btn_class': btn_class,
        'variant_id': variant_id,
        'btn_text': btn_text
    }
