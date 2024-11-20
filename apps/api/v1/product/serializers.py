from rest_framework import serializers
from .models import Product
from apps.api.v1.category.models import Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
