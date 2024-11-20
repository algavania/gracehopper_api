from django.test import TestCase
from apps.api.v1.category.models import Category


class CategoryModelTest(TestCase):

    def test_category_creation(self):

        category = Category.objects.create(
            name="Test Category", description="A sample category.")

        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "A sample category.")

        self.assertTrue(Category.objects.filter(name="Test Category").exists())

    def test_category_str_method(self):

        category = Category.objects.create(
            name="Test Category", description="A sample category.")

        self.assertEqual(str(category), "Test Category")

    def test_category_name_max_length(self):

        category = Category(name="a" * 255)
        category.save()

        self.assertEqual(category.name, "a" * 255)

    def test_category_description_nullable(self):

        category = Category.objects.create(
            name="Test Category", description=None)

        self.assertIsNone(category.description)

    def test_category_description_default_null(self):

        category = Category.objects.create(name="Test Category")

        self.assertIsNone(category.description)
