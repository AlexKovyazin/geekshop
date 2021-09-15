from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from products.models import Products
from basket.models import Basket


@login_required
def basket_add(request, product_id):
    product = Products.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        update_basket = basket.first()
        update_basket.quantity += 1
        update_basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, basket_id, quantity):
    if request.is_ajax():
        selected_basket = Basket.objects.get(id=basket_id)
        if quantity > 0:
            selected_basket.quantity = quantity
            selected_basket.save()
        else:
            selected_basket.delete()

        basket = Basket.objects.select_related('user').filter(user=request.user)
        total_sum = 0
        total_quantity = 0
        for item in basket:
            total_sum += item.sum()
            total_quantity += item.quantity

        context = {
            'basket': basket,
            'basket_total_sum': total_sum,
            'basket_total_quantity': total_quantity,
        }
        result = render_to_string('basket/basket.html', context)
        return JsonResponse({'result': result})
