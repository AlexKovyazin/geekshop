from django.conf import settings
from django.db import models

from products.models import Products


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создан'
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='обновлен'
    )
    status = models.CharField(
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING,
        verbose_name='статус'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='активен'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def get_total_quantity(self):
        items = self.order_items.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.order_items.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.order_items.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self):
        items = self.order_items.select_related()
        for item in items:
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='заказ'
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name='продукт')

    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='количество'
    )

    def get_product_cost(self):
        return self.product.price * self.quantity
