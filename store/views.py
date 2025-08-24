from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from .models import Product
from .cart import Cart


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

# --- Cart Views ---

@require_POST
def add_to_cart(request, product_id):
    """View to add a product to the cart or update its quantity."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # For simplicity, we'll handle a quantity of 1 for now.
    # A form would be needed for the user to specify a quantity.
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    return redirect('cart_detail')

@require_POST
def remove_from_cart(request, product_id):
    """View to remove a product from the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    """View to display the contents of the cart."""
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})
