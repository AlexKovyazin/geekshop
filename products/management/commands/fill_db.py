from django.core.management.base import BaseCommand
import json
import os

from users.models import User
from products.models import ProductsCategory, Products

JSON_PATH = 'products/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductsCategory.objects.all().delete()
        for category in categories:
            new_category = ProductsCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Products.objects.all().delete()
        for product in products:
            category_name = product['category']

            _category = ProductsCategory.objects.get(name=category_name)
            product['category'] = _category
            new_product = Products(**product)
            new_product.save()

        User.objects.create_superuser('AlexK',
                                      email='kovyazin.alexander@gmail.com',
                                      password='pbkdf2_sha256$260000$sa3ZLtkjOOFAvxK635BVBO$GicVRVaaZUBIurJpfm62HbwnZANCP6BzpKQjfxgnnHQ=')
