from django.shortcuts import render
from django.views.generic import ListView

from orders.models import Order


class OrdersList(ListView):
    model = Order
    extra_context = {'title': 'GeekShop - Заказы'}
    template_name = 'orders/user-order-list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class AdminOrdersList(ListView):
    model = Order
    extra_context = {'title': 'Админ-панель - Заказы'}
    template_name = 'orders/admin-order-list.html'
