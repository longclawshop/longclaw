from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (4, 1):
    from wagtail.test.utils import WagtailPageTestCase as TestCase
elif WAGTAIL_VERSION >= (3, 0) and WAGTAIL_VERSION < (4, 1):
    from wagtail.test.utils import WagtailPageTests as TestCase
else:
    from wagtail.tests.utils import WagtailPageTests as TestCase


class TestAdmin(TestCase):
    if WAGTAIL_VERSION >= (4, 1):

        def setUp(self):
            super().setUp()
            self.login()

    def test_admin(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
