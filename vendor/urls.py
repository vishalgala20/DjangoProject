from django.urls import path
from .views import VendorListCreateView, VendorDetailView

app_name = 'vendor'

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
]
