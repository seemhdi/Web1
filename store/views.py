from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
import os
from django.contrib.auth import views as auth_views
from django.db import transaction
from django.views.generic import ListView, DetailView
from .models import Product, Order, OrderItem, Category, Review
from .cart import Cart
from .forms import SignUpForm, CustomAuthenticationForm, CheckoutForm, ReviewForm


class ProductListView(ListView):
    """View to display a list of all products on the homepage."""
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().filter(status='active')
        category_slug = self.request.GET.get('category')
        sort_by = self.request.GET.get('sort')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'date_desc':
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent=None) # Top-level categories
        context['current_category'] = self.request.GET.get('category', '')
        context['current_sort'] = self.request.GET.get('sort', '')
        return context

class ProductDetailView(DetailView):
    """View to display the details of a single product."""
    model = Product
    context_object_name = 'product'

    def get_template_names(self):
        if self.object.is_code_product:
            return ['store/code_product_detail.html']
        return ['store/product_detail.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = self.object
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=self.object.pk)

        context = self.get_context_data()
        context['review_form'] = form # Show form with errors
        return self.render_to_response(context)

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
                # Don't clear the cart yet. Clear it after successful "payment".
                # Redirect to the payment simulation page
                return redirect('payment_simulation')
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

@login_required
def payment_simulation(request):
    cart = Cart(request)
    # In a real app, the order would be passed via URL or session
    # For this simulation, we'll just get the user's most recent pending order.
    order = request.user.orders.filter(status='pending').order_by('-created_at').first()

    if request.method == 'POST':
        if order:
            order.status = 'completed'
            # In a real app, you would also link a payment ID here.
            order.save()
            cart.clear() # Clear the cart after successful "payment"
            return redirect('order_complete')

    return render(request, 'store/payment_simulation.html', {'order': order})

# --- Static Pages ---
class AboutView(generic.TemplateView):
    template_name = "store/about.html"

class ContactView(generic.TemplateView):
    template_name = "store/contact.html"

class LegalView(generic.TemplateView):
    template_name = "store/legal.html"

@login_required
def download_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_code_product=True)

    # Check if the user has a completed order for this product
    has_purchased = Order.objects.filter(
        user=request.user,
        status='completed',
        items__product=product
    ).exists()

    if not has_purchased:
        raise Http404("You have not purchased this item or the order is not complete.")

    file_path = product.source_file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404("File not found.")
