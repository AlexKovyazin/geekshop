from django.contrib import admin

from products.models import Products, ProductsCategory

admin.site.register(ProductsCategory)
admin.site.register(Products)

