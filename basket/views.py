from django.shortcuts import render, HttpResponseRedirect

from products.models import Products
from basket.models import Basket


def basket_add(request, product_id):
    product = Products.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, products=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, products=product, quantity=1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        update_basket = basket.first()
        update_basket.quantity += 1
        update_basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
