from longclaw.longclawproducts import models
from longclaw.utils import maybe_get_product_model
from wagtail.tests.utils import WagtailPageTests

from longclaw.tests.products.models import ProductIndex

class TestProducts(WagtailPageTests):

    def setUp(self):
        self.product_model = maybe_get_product_model()

    def test_can_create_product(self):
        print('PRODUCT', self.product_model)
        self.assertCanCreateAt(ProductIndex, self.product_model)

    def test_variant_price(self):
        product = self.product_model(title="test", description="test")
