import os
from django import template
from longclaw import settings

register = template.Library()

CLIENT_PATH = os.path.join('core', 'js', 'longclawclient.bundle.js')
VENDORS_PATH = os.path.join('core', 'js', 'vendors.bundle.js')

@register.inclusion_tag("core/script.html")
def longclaw_vendors_bundle():
    return {'path': VENDORS_PATH}

@register.inclusion_tag("core/script.html")
def longclaw_client_bundle():
    return {'path': CLIENT_PATH}

@register.simple_tag
def longclaw_api_url_prefix():
    return settings.API_URL_PREFIX


