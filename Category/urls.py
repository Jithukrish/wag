from django.urls import path
from .api import CategoryViewSet

urlpatterns = [
    path('products_category/', CategoryViewSet.as_view({'get': 'list'}), name='product-list'),  
    path('products_category/<slug:slug>/', CategoryViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
]
