import jinja2
import jinja2.nodes
from jinja2.ext import Extension

from django.template.loader import get_template

from .templatetags.longclawcheckout_tags import gateway_client_js, gateway_token


class LongClawCheckoutExtension(Extension):
    def __init__(self, environment):
        super(LongClawCheckoutExtension, self).__init__(environment)

        self.environment.globals.update({
            'gateway_client_js': gateway_client_js,
            'gateway_token': gateway_token
        })


# Nicer import names
checkout = LongClawCheckoutExtension
