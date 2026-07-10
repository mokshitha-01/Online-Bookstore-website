from django.contrib import admin
from .models import Category, Book, Subscriber, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price', 'stock', 'is_best_seller', 'is_new_arrival', 'is_audiobook']
    list_filter = ['category', 'is_best_seller', 'is_new_arrival', 'is_audiobook', 'language']
    search_fields = ['title', 'author', 'isbn']
    list_editable = ['price', 'stock', 'is_best_seller', 'is_new_arrival']
    prepopulated_fields = {}
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'author', 'category', 'cover_image', 'description')
        }),
        ('Details', {
            'fields': ('isbn', 'publisher', 'published_date', 'pages', 'language', 'rating')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Featured Sections', {
            'fields': ('is_best_seller', 'is_new_arrival', 'is_audiobook')
        }),
        ('AI Summary', {
            'fields': ('ai_summary',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'created_at']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['book', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['full_name', 'email']
    readonly_fields = ['session_key', 'total_amount', 'created_at']
    inlines = [OrderItemInline]
    list_editable = ['status']

    fieldsets = (
        ('Customer Info', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Shipping', {
            'fields': ('address', 'city', 'pincode')
        }),
        ('Order Info', {
            'fields': ('total_amount', 'status', 'created_at', 'session_key')
        }),
    )


admin.site.site_header = "📚 BookVerse Admin"
admin.site.site_title = "BookVerse"
admin.site.index_title = "Welcome to BookVerse Admin Panel"
