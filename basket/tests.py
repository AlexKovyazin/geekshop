import decimal

from django.core.management import call_command
from django.test import TestCase

from basket.models import Basket
from products.models import Products, ProductsCategory
from users.models import User
from django.core.management import call_command
from django.test.client import Client


class TestBasketModels(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.user = User.objects.create_user(username='PekMek',
                                             email='PekMek@gmail.com',
                                             password='TestCase144')

        self.client.login(username='PekMek', password='TestCase144')

        # user_1 = User.objects.create_user(
        #     username='Alex',
        #     email='buben@mail.ru')
        #
        # user_2 = User.objects.create_user(
        #     username='Ivan',
        #     email='ivan@mail.ru')

        category_1 = ProductsCategory.objects.create(
            name='обувь')

        category_2 = ProductsCategory.objects.create(
            name='украшения')

        product_1 = Products.objects.create(
            name='кеды adidas',
            price=4500,
            quantity=100,
            category=category_1)

        product_2 = Products.objects.create(
            name='кольцо серебряное',
            price=3800,
            quantity=15,
            category=category_2)

        basket_1 = Basket.objects.create(
            user=self.user,
            product=product_1,
            quantity=2)

        basket_2 = Basket.objects.create(
            user=self.user,
            product=product_2,
            quantity=1)

    def test_str(self):
        product_1 = Products.objects.get(name='кеды adidas')
        product_2 = Products.objects.get(name='кольцо серебряное')
        basket_1 = Basket.objects.get(product=product_1)
        basket_2 = Basket.objects.get(product=product_2)

        self.assertEqual(str(basket_1), 'Корзина пользователя PekMek | Продукт кеды adidas | Кол-во 2')
        self.assertEqual(str(basket_2), 'Корзина пользователя PekMek | Продукт кольцо серебряное | Кол-во 1')

    def test_sum(self):
        product_1 = Products.objects.get(name='кеды adidas')
        product_2 = Products.objects.get(name='кольцо серебряное')
        basket_1 = Basket.objects.get(product=product_1)
        basket_2 = Basket.objects.get(product=product_2)

        self.assertIsInstance(basket_1.sum(), decimal.Decimal)
        self.assertIsInstance(basket_2.sum(), decimal.Decimal)

        self.assertEqual(basket_1.sum(), basket_1.quantity * basket_1.product.price)
        self.assertEqual(basket_2.sum(), basket_2.quantity * basket_2.product.price)

    def test_get_item(self):
        product_1 = Products.objects.get(name='кеды adidas')
        product_2 = Products.objects.get(name='кольцо серебряное')
        basket_1 = Basket.objects.get(product=product_1)
        basket_2 = Basket.objects.get(product=product_2)

        self.assertIsInstance(basket_1.get_item(basket_1.id), Basket)
        self.assertIsInstance(basket_1.get_item(basket_2.id), Basket)

        self.assertEqual(basket_1.get_item(basket_1.id), basket_1)
        self.assertEqual(basket_2.get_item(basket_2.id), basket_2)

    def tearDown(self):
        call_command('sqlsequencereset', 'products', 'users', 'orders', 'basket')

