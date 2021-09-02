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

    @staticmethod
    def get_item(pk):
        # print(Basket.objects.filter(pk=pk).first)
        return Basket.objects.get(pk=pk)
