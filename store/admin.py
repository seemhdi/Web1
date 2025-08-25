from django.contrib import admin
from .models import Category, Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """Allows editing of OrderItems from the Order page."""
    model = OrderItem
    # 'extra' determines how many blank extra forms are displayed
    extra = 0
    # Make some fields read-only in the inline view
    readonly_fields = ('product', 'price', 'quantity')
    # Prevent adding new items to an existing order via admin
    can_delete = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin view for Categories."""
    list_display = ('name', 'parent', 'slug')
    # Prepopulate the slug field from the name field
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin view for Products."""
    list_display = ('name', 'category', 'price', 'status', 'is_code_product')
    list_filter = ('category', 'status', 'is_code_product')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'category', 'status')
        }),
        ('Code Product Options', {
            'classes': ('collapse',),
            'fields': ('is_code_product', 'demo_video', 'source_file'),
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin view for Orders."""
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]
    # Make all fields read-only to prevent accidental modification
    readonly_fields = ('user', 'total_amount', 'payment_method', 'created_at')

    def has_add_permission(self, request):
        # Disable the ability to add orders manually from the admin
        return False

# We are using OrderItemInline within OrderAdmin, so a separate registration is not needed
# unless we want to manage them independently. For this scope, it's not required.
# admin.site.register(OrderItem)
