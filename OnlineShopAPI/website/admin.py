from django.contrib import admin

from .models import *


@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number', 'postal_code']
    search_fields = ['username', 'phone_number', 'postal_code',
                     'first_name', 'last_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'en_name']
    prepopulated_fields = {'slug': ('en_name',)}
    search_fields = ['name', 'en_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'title', 'brand', 'category', 'price',
                    'has_off', 'price_after_off', 'created_at']
    list_filter = ['brand', 'category', 'has_off']
    readonly_fields = ['created_at']
    search_fields = ['product_code', 'title', 'brand', 'category']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'image_number']
    list_filter = ['product']
    search_fields = ['product', 'image']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'title', 'rate', 'created_at']
    list_filter = ['product', 'user', 'rate']
    readonly_fields = ['created_at']
    search_fields = ['product', 'user', 'title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'total_price', 'status', 'track_code', 'created_at']
    list_filter = ['user', 'product', 'status']
    search_fields = ['user', 'product', 'status', 'track_code']
    readonly_fields = ['track_code']
