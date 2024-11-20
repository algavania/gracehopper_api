from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from apps.api.v1.category.models import Category
from apps.api.constants.redis import REDIS_KEY_CATEGORIES


class CategoryViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category_url = "/api/v1/categories/"
        self.detail_url = lambda id: f"/api/v1/categories/{id}/"
        self.category_data = {"name": "Test Category"}
        self.category = Category.objects.create(name="Existing Category")
        cache.clear()

    def test_get_category_list(self):
        """Test retrieving the list of categories."""
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.json())
        self.assertIn("count", response.json())

    def test_get_category_list_cached(self):
        """Test retrieving the list of categories from cache."""
        cache_key = f"{REDIS_KEY_CATEGORIES}:page=1"
        mock_cached_data = {
            "success": True,
            "message": "Categories retrieved successfully.",
            "data": [
                {"id": self.category.id, "name": self.category.name, "description": self.category.description},
            ],
            "count": 1,
            "next": None,
            "previous": None,
        }
        cache.set(cache_key, mock_cached_data)

        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), mock_cached_data)

    def test_create_category(self):
        """Test creating a category."""
        response = self.client.post(self.category_url, self.category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["data"]["name"], self.category_data["name"])

    def test_get_category_detail(self):
        """Test retrieving a category by ID."""
        response = self.client.get(self.detail_url(self.category.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["name"], self.category.name)

    def test_get_category_detail_not_found(self):
        """Test retrieving a non-existent category."""
        response = self.client.get(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category(self):
        """Test updating a category."""
        updated_data = {"name": "Updated Category"}
        response = self.client.put(self.detail_url(self.category.id), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["name"], updated_data["name"])

    def test_update_category_not_found(self):
        """Test updating a non-existent category."""
        updated_data = {"name": "Updated Category"}
        response = self.client.put(self.detail_url(9999), updated_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_category(self):
        """Test deleting a category."""
        response = self.client.delete(self.detail_url(self.category.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_delete_category_not_found(self):
        """Test deleting a non-existent category."""
        response = self.client.delete(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_cache_invalidation_on_create(self):
        """Test that the cache is invalidated when a new category is created."""
        cache_key = f"{REDIS_KEY_CATEGORIES}:page=1"
        cache.set(cache_key, {"data": "cached data"})
        self.client.post(self.category_url, self.category_data)
        self.assertIsNone(cache.get(cache_key))

    def test_category_cache_invalidation_on_update(self):
        """Test that the cache is invalidated when a category is updated."""
        cache_key = f"{REDIS_KEY_CATEGORIES}:page=1"
        cache.set(cache_key, {"data": "cached data"})
        updated_data = {"name": "Updated Category"}
        self.client.put(self.detail_url(self.category.id), updated_data)
        self.assertIsNone(cache.get(cache_key))

    def test_category_cache_invalidation_on_delete(self):
        """Test that the cache is invalidated when a category is deleted."""
        cache_key = f"{REDIS_KEY_CATEGORIES}:page=1"
        cache.set(cache_key, {"data": "cached data"})
        self.client.delete(self.detail_url(self.category.id))
        self.assertIsNone(cache.get(cache_key))
