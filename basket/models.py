from django.db import models

from users.models import User
from products.models import Products


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина пользователя {self.user.username} | Продукт {self.product.name} | Кол-во {self.quantity}'

    def sum(self):
        return self.quantity * self.product.price

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
