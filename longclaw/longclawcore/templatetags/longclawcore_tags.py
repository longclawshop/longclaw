from django import template

register = template.Library()

@register.inclusion_tag("longclawcore/script.html")
def vendors_bundle():
    return {'path': 'longclawcore/js/vendors.bundle.js'}

@register.inclusion_tag("longclawcore/script.html")
def client_bundle():
    return {'path': 'longclawcore/js/longclawclient.bundle.js'}
