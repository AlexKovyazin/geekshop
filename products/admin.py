from django.contrib import admin

from products.models import Products, ProductsCategory


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category', 'is_active')
    search_fields = ('id', 'name', 'price', 'quantity', 'category', 'is_active')


@admin.register(ProductsCategory)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active',)
    search_fields = ('id', 'name', 'is_active',)
