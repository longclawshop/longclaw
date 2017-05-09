from django import template
from longclaw.longclawbasket.utils import get_basket_items

register = template.Library()

@register.simple_tag(takes_context=True)
def basket(context):
    '''
    Return the BasketItems in the current basket
    '''
    items, _ = get_basket_items(context["request"])
    return items
