from django.contrib import admin

from .models import *


@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number', 'postal_code']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'en_name']
    prepopulated_fields = {'slug': ('en_name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'title', 'brand', 'category', 'price', 'has_off', 'price_after_off']
    list_filter = ['brand', 'category', 'has_off']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'image_number']
    list_filter = ['product']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'title', 'rate']
    list_filter = ['product', 'user', 'rate']
