from django.contrib import admin

from products.models import Products, ProductsCategory

admin.site.register(ProductsCategory)


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'description', 'price', 'quantity', 'category')
    ordering = ('name',)
    search_fields = ('name',)
