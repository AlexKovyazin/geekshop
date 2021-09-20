from django.contrib import admin

from products.models import Products, ProductsCategory

admin.site.register(ProductsCategory)


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category', 'is_active')
    ordering = ('name',)
    search_fields = ('id', 'name', 'price', 'quantity', 'category', 'is_active')
