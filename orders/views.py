from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basket.models import Basket
from orders.forms import OrderItemForm
from orders.models import Order, OrderItem


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


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:OrdersList')
    template_name = 'orders/order-form.html'

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = order_formset(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = order_formset()
                for i, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[i].products
                    form.initial['quantity'] = basket_items[i].quantity
                basket_items.delete()
            else:
                formset = order_formset()

        data['order_items'] = formset
        data['user_basket'] = Basket.objects.filter(user=self.request.user)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:OrdersList')

    def get_context_data(self, **kwargs):
        data = super(OrderUpdate, self).get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = order_formset(self.request.POST, instance=self.object)
        else:
            formset = order_formset(instance=self.object)

            data['order_items'] = formset

            return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders:OrdersList')
    template_name = 'orders/order-confirm-delete.html'


class OrderRead(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order-details.html'

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:OrdersList'))
