from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Model for product categories."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # The design shows nested categories, so a parent relationship is needed.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Correct plural name in admin
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    """Model for digital products."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    # Using URLField for now as placeholders, will be replaced by File/Image fields later.
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    download_url = models.URLField(max_length=1024)
    status_choices = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    # Fields for code-based products
    is_code_product = models.BooleanField(default=False)
    demo_video = models.FileField(upload_to='products/videos/', blank=True, null=True)
    source_file = models.FileField(upload_to='products/source/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    """Model for customer orders."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    """Model for items within an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # Prevent product deletion if it's in an order
    quantity = models.PositiveIntegerField(default=1)
    # Store the price at the time of purchase
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

class Review(models.Model):
    """Model for product reviews."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)]) # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user') # Each user can only review a product once
        ordering = ('-created_at',)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'
