from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    # Using 'home' as the name for the root URL of the store
    path('', ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
