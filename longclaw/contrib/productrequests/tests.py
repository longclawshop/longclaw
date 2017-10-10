from longclaw.tests.utils import LongclawTestCase, ProductVariantFactory
from longclaw.contrib.productrequests.models import ProductRequest
from longclaw.contrib.productrequests.templatetags import productrequests_tags

class ProductRequestTest(LongclawTestCase):

    def setUp(self):
        self.variant = ProductVariantFactory()
        self.product_request = ProductRequest(variant=self.variant)

    def test_get_request(self):
        self.get_test('productrequests_list')

    def test_post_request(self):
        self.post_test({'variant_id': self.variant.id}, 'productrequests_list')

    def test_get_variant_requests(self):
        self.get_test(
            'productrequests_variant_list',
            {'variant_id': self.variant.id}
        )

    def test_make_rquest_btn(self):
        result = productrequests_tags.make_request_btn(1)
        self.assertIsNotNone(result)

    def test_get_admin(self):
        """Check we can retrieve the requests admin page
        """
        self.get_test('productrequests_admin', {'pk': self.variant.product.id})
