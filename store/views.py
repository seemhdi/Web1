from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    """View to display a list of all products on the homepage."""
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    """View to display the details of a single product."""
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
