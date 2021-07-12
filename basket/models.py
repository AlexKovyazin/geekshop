from django.db import models

from users.models import User
from products.models import Products


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина пользователя {self.user.username} | Продукт {self.products.name} | Кол-во {self.quantity}'

    def sum(self):
        return self.quantity * self.products.price

    def total_quantity(self):
        result = 0
        for basket in Basket.objects.filter(user=self.user):
            result += basket.quantity
        return result

    def total_sum(self):
        result = 0
        for basket in Basket.objects.filter(user=self.user):
            result += basket.sum()
        return result
