from django.core.cache import cache

from geekshop import settings
from products.models import Products, ProductsCategory
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection


class ProductsIndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'GeekShop'
        return context


class ProductsListView(ListView):
    model = Products
    context_object_name = 'products'
    paginate_by = 6
    template_name = 'products/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GeekShop - Каталог'
        context['ProductsCategory'] = self.get_categories()
        return context

    def get_queryset(self):
        if 'category_id' in self.kwargs:
            chosen_category_id = self.kwargs['category_id']
        else:
            chosen_category_id = None
        if settings.LOW_CACHE:
            if chosen_category_id:
                key = f'products_{chosen_category_id}'
                products = cache.get(key)
                if products is None:
                    products = Products.objects.filter(category_id=chosen_category_id)
                    cache.set(key, products)
            else:
                key = 'products'
                products = cache.get(key)
                if products is None:
                    products = Products.objects.all()
                    cache.set(key, products)

        else:
            if not chosen_category_id:
                products = Products.objects.all()
            else:
                products = Products.objects.filter(category_id=chosen_category_id)

        return products

    @staticmethod
    def get_categories():
        if settings.LOW_CACHE:
            key = 'categories'
            categories = cache.get(key)
            if categories is None:
                categories = ProductsCategory.objects.all()
                cache.set(key, categories)
            return categories
        else:
            return ProductsCategory.objects.all()


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductsCategory)
def product_products_category_is_active_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.products_set.update(is_active=True)
        else:
            instance.products_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
