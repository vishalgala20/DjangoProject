from django.urls import path
from .views import ProductListCreateView, ProductDetailView

app_name = 'product'

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
