import jinja2
import jinja2.nodes
from jinja2.ext import Extension

from django.template.loader import get_template

# to keep namespaces from colliding
from .templatetags import longclawcore_tags as lc_tags


def longclaw_vendors_bundle():
    template = get_template('core/longclaw_script.html')

    context = lc_tags.longclaw_vendors_bundle()

    return template.render(context=context)


def longclaw_client_bundle():
    template = get_template('core/longclaw_script.html')

    context = lc_tags.longclaw_client_bundle()

    return template.render(context=context)


class LongClawCoreExtension(Extension):
    def __init__(self, environment):
        super(LongClawCoreExtension, self).__init__(environment)

        self.environment.globals.update({
            'longclaw_api_url_prefix': lc_tags.longclaw_api_url_prefix,
            'longclaw_client_bundle': longclaw_client_bundle,
            'longclaw_vendors_bundle': longclaw_vendors_bundle,
        })


# Nicer import names
core = LongClawCoreExtension
