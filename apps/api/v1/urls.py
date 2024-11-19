from django.urls import path, include

urlpatterns = [
    path('categories/', include('apps.api.v1.category.urls')),
    path('products/', include('apps.api.v1.product.urls')),
]
