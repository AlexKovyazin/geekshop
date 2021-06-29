from django.shortcuts import render
import os
import json
from geekshop.settings import BASE_DIR


def index(request):
    context = {
        'title': 'Geekshop'
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Catalog'
    }
    with open(BASE_DIR / 'products/fixtures/goods.json', 'r', encoding='UTF-8') as goods:
        context['products'] = json.load(goods)

    return render(request, 'products/products.html', context)
