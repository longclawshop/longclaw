from django import template
from longclaw import settings

register = template.Library()

@register.inclusion_tag("core/script.html")
def longclaw_vendors_bundle():
    return {'path': 'core/js/vendors.bundle.js'}

@register.inclusion_tag("core/script.html")
def longclaw_client_bundle():
    return {'path': 'core/js/longclawclient.bundle.js'}

@register.simple_tag
def longclaw_api_url_prefix():
    return settings.API_URL_PREFIX
