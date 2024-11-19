from django.urls import path, include

urlpatterns = [
    path('categories/', include('apps.api.v1.category.urls')),
]
