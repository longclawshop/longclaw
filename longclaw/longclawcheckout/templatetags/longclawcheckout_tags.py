from django import template
from longclaw.longclawcheckout.utils import GATEWAY

register = template.Library()

@register.simple_tag
def gateway_client_js():
    '''
    Template tag which provides a `script` tag for each javascript item
    required by the payment gateway
    '''
    javascripts = GATEWAY.client_js()
    if isinstance(javascripts, (tuple, list)):
        tags = []
        for js in javascripts:
            tags.append('<script type="text/javascript" src="{}"></script>'.format(js))
        return tags
    else:
        raise TypeError(
            'function client_js of {} must return a list or tuple'.format(GATEWAY.__name__))


@register.simple_tag
def gateway_token():
    '''
    Provide a client token from the chosen gateway
    '''
    return GATEWAY.get_token()
