from django.urls import path
from .api import ProductCategoryViewSet

urlpatterns = [
    path('products/', ProductCategoryViewSet.as_view({'get': 'list'}), name='product-list'),
    # path('products/<slug:slug>/', ProductCategoryViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
    path('products/<int:pk>/', ProductCategoryViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
]
