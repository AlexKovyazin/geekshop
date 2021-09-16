from django.core.cache import cache
import logging

from geekshop import settings
from products.models import Products, ProductsCategory
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from products.mixins import CacheMixin


class ProductsIndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'GeekShop'
        return context


class ProductsListView(CacheMixin, ListView):
    model = Products
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'products/products.html'
    logger = logging.getLogger(__name__)

    logger.error('test!')
    logger.debug('test debug msg!')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GeekShop - Каталог'
        context['ProductsCategory'] = self.get_categories()
        return context

    def get_queryset(self):
        if settings.LOW_CACHE:
            key = 'products'
            products = cache.get(key)
            if products is None:
                if 'category_id' not in self.kwargs:
                    products = Products.objects.all()
                else:
                    products =  Products.objects.filter(category_id=self.kwargs['category_id'])
                cache.set(key, products)
            return products
        else:
            if 'category_id' not in self.kwargs:
                products = Products.objects.all()
            else:
                products = Products.objects.filter(category_id=self.kwargs['category_id'])
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



