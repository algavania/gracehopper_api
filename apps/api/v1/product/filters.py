import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains', label='Category')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Price Min')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Price Max')

    class Meta:
        model = Product
        fields = ['category', 'price_min', 'price_max']
