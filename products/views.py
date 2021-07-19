from django.shortcuts import render
from products.models import Products, ProductsCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = {
        'title': 'Geekshop'
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    context = {
        'title': 'GeekShop - Каталог',
        'ProductsCategory': ProductsCategory.objects.all(),
    }
    if category_id:
        items = Products.objects.filter(category_id=category_id)
    else:
        items = Products.objects.all()

    paginator = Paginator(items, 3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator

    return render(request, 'products/products.html', context)
