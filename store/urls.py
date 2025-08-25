from django.urls import path
from . import views

urlpatterns = [
    # Using 'home' as the name for the root URL of the store
    path('', views.ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Cart URLs
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Auth URLs
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
