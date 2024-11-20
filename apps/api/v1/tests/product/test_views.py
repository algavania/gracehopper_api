from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from apps.api.v1.product.models import Product
from apps.api.v1.category.models import Category
from apps.api.constants.redis import REDIS_KEY_PRODUCTS


class ProductViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        category = Category.objects.create(name="Test Category")
        self.product_url = "/api/v1/products/"
        self.detail_url = lambda id: f"/api/v1/products/{id}/"
        self.product_data = {"name": "Test Product",
                             "price": 100.0, "category": category.id}
        self.product = Product.objects.create(
            name="Existing Product", price=50.0, category=category)
        cache.clear()

    def test_get_product_list(self):
        """Test retrieving the list of products."""
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.json())
        self.assertIn("count", response.json())

    def test_get_product_list_cached(self):
        """Test retrieving the list of products from cache."""
        cache_key = f"{REDIS_KEY_PRODUCTS}:page=1"
        mock_cached_data = {
            "success": True,
            "message": "Products retrieved successfully.",
            "data": [
                {
                    "id": self.product.id,
                    "name": self.product.name,
                    "description": self.product.description,
                    "price": self.product.price,
                    "created_at": self.product.created_at.isoformat(),
                    "updated_at": self.product.updated_at.isoformat(),
                    "category": self.product.category.id,
                },
            ],
            "count": 1,
            "next": None,
            "previous": None,
        }
        cache.set(cache_key, mock_cached_data)

        response = self.client.get(self.product_url)
        mock_cached_data['data'][0]['created_at'] = response.json()['data'][0]['created_at']
        mock_cached_data['data'][0]['updated_at'] = response.json()['data'][0]['updated_at']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), mock_cached_data)

    def test_create_product(self):
        """Test creating a product."""
        response = self.client.post(self.product_url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["data"]
                         ["name"], self.product_data["name"])

    def test_get_product_detail(self):
        """Test retrieving a product by ID."""
        response = self.client.get(self.detail_url(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["name"], self.product.name)

    def test_get_product_detail_not_found(self):
        """Test retrieving a non-existent product."""
        response = self.client.get(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        """Test updating a product."""
        updated_data = {"name": "Updated Product",
                        "price": 120.0, "category": self.product.category.id}
        response = self.client.put(
            self.detail_url(self.product.id), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["name"], updated_data["name"])

    def test_update_product_not_found(self):
        """Test updating a non-existent product."""
        updated_data = {"name": "Updated Product", "price": 120.0}
        response = self.client.put(self.detail_url(9999), updated_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product(self):
        """Test deleting a product."""
        response = self.client.delete(self.detail_url(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_delete_product_not_found(self):
        """Test deleting a non-existent product."""
        response = self.client.delete(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_cache_invalidation_on_create(self):
        """Test that the cache is invalidated when a new product is created."""
        cache_key = f"{REDIS_KEY_PRODUCTS}:page=1"
        cache.set(cache_key, {"data": "cached data"})
        self.client.post(self.product_url, self.product_data)
        self.assertIsNone(cache.get(cache_key))

    def test_product_cache_invalidation_on_update(self):
        """Test that the cache is invalidated when a product is updated."""
        cache_key = f"{REDIS_KEY_PRODUCTS}:page=1"
        cache.set(cache_key, {"data": "cached data"})
        updated_data = {"name": "Updated Product", "price": 120.0, "category": self.product.category.id}
        self.client.put(self.detail_url(self.product.id), updated_data)
        self.assertIsNone(cache.get(cache_key))

    def test_product_cache_invalidation_on_delete(self):
        """Test that the cache is invalidated when a product is deleted."""
        cache_key = f"{REDIS_KEY_PRODUCTS}:page=1"
        cache.set(cache_key, {"data": "cached data"})
        self.client.delete(self.detail_url(self.product.id))
        self.assertIsNone(cache.get(cache_key))
