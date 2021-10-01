import decimal

from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

from orders.models import OrderItem, Order
from products.models import ProductsCategory, Products
from users.models import User


class TestOrdersModels(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.user = User.objects.create_user(username='PekMek',
                                             email='PekMek@gmail.com',
                                             password='TestCase144')

        self.client.login(username='PekMek', password='TestCase144')

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

        order_1 = Order.objects.create(
            user=self.user)

        order_item_1 = OrderItem.objects.create(
            order=order_1,
            product=Products.objects.get(name='кеды adidas'),
            quantity=2)

    def test_Order_str(self):
        order_1 = Order.objects.create(
            user=self.user)

        self.assertIsInstance(str(order_1), str)
        self.assertEqual(str(order_1), f'Текущий заказ: {order_1.id}')

    def test_Order_delete(self):
        product_1_quantity_before = int(Products.objects.get(name='кеды adidas').quantity)
        product_2_quantity_before = int(Products.objects.get(name='кольцо серебряное').quantity)

        order_1 = Order.objects.create(
            user=self.user)
        order_item_1 = OrderItem.objects.create(
            order=order_1,
            product=Products.objects.get(name='кеды adidas'),
            quantity=2)
        order_item_2 = OrderItem.objects.create(
            order=order_1,
            product=Products.objects.get(name='кольцо серебряное'),
            quantity=1)

        self.assertTrue(order_1.is_active)
        self.assertLess(Products.objects.get(name='кеды adidas').quantity, product_1_quantity_before)
        self.assertLess(Products.objects.get(name='кольцо серебряное').quantity, product_2_quantity_before)
        order_1.delete()
        self.assertFalse(order_1.is_active)
        self.assertEqual(Products.objects.get(name='кеды adidas').quantity, product_1_quantity_before)
        self.assertEqual(Products.objects.get(name='кольцо серебряное').quantity, product_2_quantity_before)

    def test_Order_get_total_cost(self):
        order_1 = Order.objects.create(
            user=self.user)
        order_item_1 = OrderItem.objects.create(
            order=order_1,
            product=Products.objects.get(name='кеды adidas'),
            quantity=2)
        order_item_2 = OrderItem.objects.create(
            order=order_1,
            product=Products.objects.get(name='кольцо серебряное'),
            quantity=1)

        self.assertIsInstance(order_1.get_total_cost(), decimal.Decimal)
        self.assertEqual(
            order_1.get_total_cost(),
            order_item_1.product.price * order_item_1.quantity + order_item_2.product.price * order_item_2.quantity)

    def test_OrderItem_get_product_cost(self):
        order_1 = Order.objects.create(
            user=self.user)
        order_item_1 = OrderItem.objects.create(
            order=order_1,
            product=Products.objects.get(name='кеды adidas'),
            quantity=2)

        self.assertIsInstance(order_item_1.get_product_cost(), decimal.Decimal)
        self.assertEqual(order_item_1.get_product_cost(), order_item_1.product.price * order_item_1.quantity)

    def test_OrderItem_str(self):
        order_1 = Order.objects.create(
            user=self.user)

        order_item_1 = OrderItem.objects.create(
            order=order_1,
            product=Products.objects.get(name='кеды adidas'),
            quantity=2)

        self.assertIsInstance(str(order_item_1), str)
        self.assertEqual(str(order_item_1), f'{order_item_1.product.name}')
