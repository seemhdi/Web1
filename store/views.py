from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.db import transaction
from django.views.generic import ListView, DetailView
from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import SignUpForm, CustomAuthenticationForm, CheckoutForm


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

# --- User Account Views ---

@login_required
def dashboard(request):
    return render(request, 'store/dashboard.html', {'section': 'dashboard'})

class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'store/signup.html'

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create the order
                    order = Order.objects.create(
                        user=request.user,
                        total_amount=cart.get_total_price(),
                        # Status will default to 'pending'
                    )
                    # Create order items
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['quantity']
                        )
                # Clear the cart
                cart.clear()
                # Redirect to a success page
                return redirect('order_complete')
            except Exception as e:
                # Handle potential errors during transaction
                # For now, just pass, but in a real app, you'd log this
                # and show an error message.
                pass
    else:
        # Pre-fill the email form with the user's email
        form = CheckoutForm(initial={'email': request.user.email})

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})

def order_complete(request):
    return render(request, 'store/order_complete.html')
