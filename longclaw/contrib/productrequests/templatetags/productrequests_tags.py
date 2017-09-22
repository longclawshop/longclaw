from django import template
register = template.Library()


@register.inclusion_tag('productrequests/make_request.html')
def make_request_btn(variant_id, btn_class="btn btn-default", btn_text="Request Product"):
    '''Button to make a new product request on a variant.
    This is a basic button which does not gather the email details for the customer making the request
    '''
    return {
        'btn_class': btn_class,
        'variant_id': variant_id,
        'btn_text': btn_text
    }
