from django.test import TestCase
from apps.api.v1.category.models import Category
from apps.api.v1.product.models import Product
from decimal import Decimal
from django.core.exceptions import ValidationError

class ProductModelTests(TestCase):
    def setUp(self):
        """Set up test dependencies."""
        self.category = Category.objects.create(name="Test Category")
        self.product_data = {
            "name": "Test Product",
            "description": "This is a test product.",
            "price": Decimal("19.99"),
            "category": self.category,
        }

    def test_create_product(self):
        """Test creating a product."""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.name, self.product_data["name"])
        self.assertEqual(product.description, self.product_data["description"])
        self.assertEqual(product.price, self.product_data["price"])
        self.assertEqual(product.category, self.category)
        self.assertIsNotNone(product.created_at)
        self.assertIsNotNone(product.updated_at)

    def test_product_str_representation(self):
        """Test the string representation of the product."""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(str(product), self.product_data["name"])

    def test_product_missing_name(self):
        """Test creating a product without a name."""
        self.product_data["name"] = ""
        product = Product(**self.product_data)
        with self.assertRaises(ValidationError) as context:
            product.full_clean()
        self.assertIn("This field cannot be blank.", str(context.exception))

    def test_product_price_validation(self):
        """Test creating a product with an invalid price."""
        self.product_data["price"] = "invalid_price"
        product = Product(**self.product_data)
        with self.assertRaises(ValidationError) as context:
            product.full_clean()
        self.assertIn("value must be a decimal number", str(context.exception))

    def test_product_foreign_key_constraint(self):
        """Test deleting a category and its impact on related products."""
        product = Product.objects.create(**self.product_data)
        self.category.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product.id)
