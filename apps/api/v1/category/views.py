from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from apps.api.utils.response_formatter import format_response
from apps.api.utils.exceptions import ApiException
from django.core.cache import cache
from apps.api.constants.redis import REDIS_KEY_CATEGORIES
from apps.api.utils.util import get_cache_key, delete_cache_by_pattern


class CategoryListView(APIView):
    def get(self, request):
        try:
            cache_key = get_cache_key(
                REDIS_KEY_CATEGORIES, request.query_params)

            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)

            categories = Category.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 10

            try:
                paginated_categories = paginator.paginate_queryset(
                    categories, request)
            except Exception as e:
                raise ApiException(
                    message=str(e),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            serializer = CategorySerializer(paginated_categories, many=True)
            paginator_data = paginator.get_paginated_response(serializer.data)

            formatted_response = format_response(
                success=True,
                message="Categories retrieved successfully.",
                data=paginator_data.data['results'],
                status_code=status.HTTP_200_OK
            )

            formatted_response.data.update({
                "count": paginator_data.data['count'],
                "next": paginator_data.data['next'],
                "previous": paginator_data.data['previous'],
            })

            cache.set(cache_key, formatted_response.data)
            return formatted_response
        except ApiException as e:
            return format_response(
                success=False,
                message=e.message,
                data=None,
                status_code=e.status_code,
            )
        except Exception as e:
            return format_response(
                success=False,
                message=str(e),
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                delete_cache_by_pattern(f"{REDIS_KEY_CATEGORIES}*")
                
                return format_response(
                    success=True,
                    message="Category created successfully.",
                    data=serializer.data,
                    status_code=status.HTTP_201_CREATED,
                )
            return format_response(
                success=False,
                message="Validation error occurred.",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return format_response(
                success=False,
                message=str(e),
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CategoryDetailView(APIView):
    def get(self, _, id):
        try:
            cache_key = get_cache_key(REDIS_KEY_CATEGORIES, {"id": id})
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            category = Category.objects.get(id=id)
            serializer = CategorySerializer(category)
            
            response = format_response(
                success=True,
                message="Category retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
            cache.set(cache_key, response.data)
            return response
        except Category.DoesNotExist:
            return format_response(
                success=False,
                message="Category not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return format_response(
                success=False,
                message=str(e),
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, id):
        try:
            category = Category.objects.get(id=id)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                delete_cache_by_pattern(f"{REDIS_KEY_CATEGORIES}*")
                return format_response(
                    success=True,
                    message="Category updated successfully.",
                    data=serializer.data,
                    status_code=status.HTTP_200_OK,
                )
            return format_response(
                success=False,
                message="Validation error occurred.",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Category.DoesNotExist:
            return format_response(
                success=False,
                message="Category not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return format_response(
                success=False,
                message=str(e),
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
            category.delete()
            delete_cache_by_pattern(f"{REDIS_KEY_CATEGORIES}*")
            return format_response(
                success=True,
                message="Category deleted successfully.",
                data=None,
                status_code=status.HTTP_204_NO_CONTENT,
            )
        except Category.DoesNotExist:
            return format_response(
                success=False,
                message="Category not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return format_response(
                success=False,
                message=str(e),
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
