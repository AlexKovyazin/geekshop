from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models.signals import pre_save, pre_delete

from basket.models import Basket
from orders.forms import OrderItemForm
from orders.models import Order, OrderItem
from products.models import Products


class OrdersList(LoginRequiredMixin, ListView):
    model = Order
    extra_context = {'title': 'GeekShop - Заказы'}
    template_name = 'orders/user-order-list.html'

    def get_queryset(self):
        return Order.objects.select_related('user').filter(user=self.request.user)


class AdminOrdersList(LoginRequiredMixin, ListView):
    model = Order
    extra_context = {'title': 'Админ-панель - Заказы'}
    template_name = 'orders/admin-order-list.html'

    def get_queryset(self):
        return Order.objects.all()


class OrderItemsCreate(LoginRequiredMixin, CreateView):
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
            basket_items = Basket.objects.filter(user=self.request.user).select_related()
            if len(basket_items):
                order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items) + 1)
                formset = order_formset()
                for i, form in enumerate(formset.forms):
                    if i == len(formset.forms) - 1:
                        break
                    else:
                        form.initial['product'] = basket_items[i].product
                        form.initial['quantity'] = basket_items[i].quantity
                        form.initial['price'] = basket_items[i].product.price
                basket_items.delete()
            else:
                formset = order_formset()

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

        return super(OrderItemsCreate, self).form_valid(form)


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:OrdersList')

    def get_context_data(self, **kwargs):
        data = super(OrderUpdate, self).get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            data['order_items'] = order_formset(self.request.POST, instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = order_formset(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

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

        items = OrderItem.objects.select_related('order').filter(order=kwargs['object'].id)
        total_quantity = sum(list(map(lambda x: x.quantity, items)))
        total_cost = sum(list(map(lambda x: x.quantity * x.product.price, items)))
        product_type_quantity = len(items)

        context = {
            **context,
            'title': 'заказ/просмотр',
            'order_total_quantity': total_quantity,
            'order_total_cost': total_cost,
            'order_product_type_quantity': product_type_quantity,
        }
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:OrdersList'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields == 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def get_product_price(request, pk):
    if request.is_ajax():
        product = Products.objects.filter(pk=int(pk)).first()
        if product:
            return JsonResponse({'price': product.price})
        else:
            return JsonResponse({'price': 0})
