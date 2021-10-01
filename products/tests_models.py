import django.db.models.query
from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

from products.models import ProductsCategory, Products
from users.models import User


class TestProductsModels(TestCase):
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

    def test_ProductsCategory_str(self):
        self.assertIsInstance(str(ProductsCategory.objects.get(name='кеды adidas')), str)
        self.assertEqual(str(ProductsCategory.objects.get(name='кеды adidas')),
                         ProductsCategory.objects.get(name='кеды adidas').name)

    def test_Products_str(self):
        self.assertIsInstance(str(Products.objects.get(name='кеды adidas')), str)
        self.assertEqual(str(Products.objects.get(name='кеды adidas')),
                         Products.objects.get(name='кеды adidas').name)

    def test_Products_get_items(self):
        print(type(Products.get_items()))
        self.assertIsInstance(Products.get_items(), django.db.models.query.QuerySet)
        self.assertIsInstance(Products.get_items()[0], Products)
