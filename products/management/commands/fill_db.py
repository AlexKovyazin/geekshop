from django.core.management.base import BaseCommand
import json
import os

from products.models import ProductsCategory, Products

JSON_PATH = 'products/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('products_productscategory')

        ProductsCategory.objects.all().delete()
        for category in categories:
            new_category = ProductsCategory(**category)
            new_category.save()

        products = load_from_json('products_products')

        Products.objects.all().delete()
        for product in products:
            new_product = Products(**product)
            new_product.save()
