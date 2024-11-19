from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from apps.api.utils.response_formatter import format_response
from apps.api.utils.exceptions import ApiException
from .filters import ProductFilter


class ProductListView(APIView):
    def get(self, request):
        try:
            filterset = ProductFilter(
                request.query_params, queryset=Product.objects.all())

            if filterset.is_valid():
                products = filterset.qs
            else:
                raise ApiException(
                    message="Invalid filter parameters.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            paginator = PageNumberPagination()
            paginator.page_size = 10

            try:
                paginated_products = paginator.paginate_queryset(
                    products, request)
            except Exception as e:
                raise ApiException(
                    message=str(e),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            serializer = ProductSerializer(paginated_products, many=True)
            paginator_data = paginator.get_paginated_response(serializer.data)

            formatted_response = format_response(
                success=True,
                message="Products retrieved successfully.",
                data=paginator_data.data['results'],
                status_code=status.HTTP_200_OK
            )

            formatted_response.data.update({
                "count": paginator_data.data['count'],
                "next": paginator_data.data['next'],
                "previous": paginator_data.data['previous'],
            })

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
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return format_response(
                    success=True,
                    message="Product created successfully.",
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


class ProductDetailView(APIView):
    def get(self, _, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return format_response(
                success=True,
                message="Product retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Product.DoesNotExist:
            return format_response(
                success=False,
                message="Product not found.",
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
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return format_response(
                    success=True,
                    message="Product updated successfully.",
                    data=serializer.data,
                    status_code=status.HTTP_200_OK,
                )
            return format_response(
                success=False,
                message="Validation error occurred.",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Product.DoesNotExist:
            return format_response(
                success=False,
                message="Product not found.",
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
            product = Product.objects.get(id=id)
            product.delete()
            return format_response(
                success=True,
                message="Product deleted successfully.",
                data=None,
                status_code=status.HTTP_204_NO_CONTENT,
            )
        except Product.DoesNotExist:
            return format_response(
                success=False,
                message="Product not found.",
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
