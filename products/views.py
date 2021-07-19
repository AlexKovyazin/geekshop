from django.shortcuts import render
from products.models import Products, ProductsCategory


def index(request):
    context = {
        'title': 'Geekshop'
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    context = {
        'title': 'Catalog',
        'ProductsCategory': ProductsCategory.objects.all(),
    }
    if category_id:
        context['products'] = Products.objects.filter(category_id=category_id)
    else:
        context['products'] = Products.objects.all()

    return render(request, 'products/products.html', context)
