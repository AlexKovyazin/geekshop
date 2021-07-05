from django.shortcuts import render
from products.models import Products, ProductsCategory


def index(request):
    context = {
        'title': 'Geekshop'
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Catalog',
        'products': Products.objects.all(),
        'ProductsCategory': ProductsCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)
