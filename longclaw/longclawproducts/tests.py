from longclaw.longclawproducts import models
from wagtail.tests.utils import WagtailPageTests

class TestProducts(WagtailPageTests):

    def test_can_create_product(self):
        self.assertCanCreateAt(models.ProductIndex, models.Product)

    def test_variant_price(self):
        product = models.Product(title="test", description="test")


