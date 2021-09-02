from products.models import Products, ProductsCategory
from django.views.generic import TemplateView
from django.views.generic.list import ListView


class ProductsIndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'GeekShop'
        return context


class ProductsListView(ListView):
    model = Products
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'products/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GeekShop - Каталог'
        context['ProductsCategory'] = ProductsCategory.objects.all()
        return context

    def get_queryset(self):
        if 'category_id' not in self.kwargs:
            return Products.objects.all()
        else:
            return Products.objects.filter(category_id=self.kwargs['category_id'])
