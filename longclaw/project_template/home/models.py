from __future__ import absolute_import, unicode_literals
try:
    from wagtail.core.models import Page
except ImportError:
    from wagtail.wagtailcore.models import Page


class HomePage(Page):
    pass
