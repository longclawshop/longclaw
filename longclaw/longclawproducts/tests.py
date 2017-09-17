from wagtail.tests.utils import WagtailPageTests
from longclaw.utils import maybe_get_product_model
from longclaw.tests.products.models import ProductIndex
from longclaw.tests.utils import ProductVariantFactory
from longclaw.longclawproducts.serializers import ProductVariantSerializer

class TestProducts(WagtailPageTests):

    def setUp(self):
        self.product_model = maybe_get_product_model()

    def test_can_create_product(self):
        self.assertCanCreateAt(ProductIndex, self.product_model)

    def test_variant_price(self):
        variant = ProductVariantFactory()
        self.assertTrue(variant.price == variant.base_price * 10)
        self.assertTrue(variant.price > 0)

    def test_price_range(self):
        variant = ProductVariantFactory()
        prices = variant.product.price_range
        self.assertTrue(prices[0] == prices[1])

    def test_stock(self):
        variant = ProductVariantFactory()
        variant.stock = 1
        variant.save()
        self.assertTrue(variant.product.in_stock)

    def test_out_of_stock(self):
        variant = ProductVariantFactory()
        variant.stock = 0
        variant.save()
        self.assertFalse(variant.product.in_stock)

    def test_variant_serializer(self):
        variant = ProductVariantFactory()
        serializer = ProductVariantSerializer(variant)
        self.assertIn('product', serializer.data)

    def test_product_title(self):
        variant = ProductVariantFactory()
        self.assertEqual(variant.get_product_title(), variant.product.title)
