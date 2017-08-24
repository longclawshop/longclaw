import os
from django.test import TestCase
from django.contrib.staticfiles import finders

from longclaw import settings
from longclaw.longclawcore.templatetags import longclawcore_tags

class TagTests(TestCase):

    def _test_static_file(self, pth):
        result = finders.find(pth)
        print(result)
        self.assertTrue(result)

    def test_vendors_bundle(self):
        ctx = longclawcore_tags.longclaw_vendors_bundle()
        self._test_static_file(ctx['path'])

    def test_client_bundle(self):
        ctx = longclawcore_tags.longclaw_client_bundle()
        self._test_static_file(ctx['path'])

    def test_api_url_prefix(self):
        self.assertEqual(
            settings.API_URL_PREFIX,
            longclawcore_tags.longclaw_api_url_prefix()
        )
