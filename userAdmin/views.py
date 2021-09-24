from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from products.models import Products, ProductsCategory
from users.models import User
from userAdmin.forms import AdminUserRegistrationForm, AdminUserUpdateForm, ProductCreateForm, ProductUpdateForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    return render(request, 'userAdmin/index.html')


# Отображение и редактирование пользователей
class UserAdminListView(ListView):
    model = User
    template_name = 'userAdmin/userAdmin-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Админ-панель - Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserAdminCreateView(CreateView):
    model = User
    form_class = AdminUserRegistrationForm
    template_name = 'userAdmin/userAdmin-create.html'
    success_url = reverse_lazy('userAdmin:users_read')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Админ-панель - Создание пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserAdminUpdateView(UpdateView):
    model = User
    form_class = AdminUserUpdateForm
    template_name = 'userAdmin/userAdmin-update-delete.html'
    success_url = reverse_lazy('userAdmin:users_read')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Админ-панель - Редактирование пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserAdminDeleteView(DeleteView):
    model = User
    template_name = 'userAdmin/userAdmin-update-delete.html'
    success_url = reverse_lazy('userAdmin:users_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# Отображение и редактирование товаров
class AdminProductsListView(LoginRequiredMixin, ListView):
    model = Products
    extra_context = {'title': 'Админ-панель - Товары'}
    template_name = 'userAdmin/products-list.html'

    def get_queryset(self):
        return Products.objects.all()


class AdminProductsCreateView(CreateView):
    model = Products
    form_class = ProductCreateForm
    template_name = 'userAdmin/products-create.html'
    success_url = reverse_lazy('products:admin_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Админ-панель - Создание товара'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductsAdminUpdateView(UpdateView):
    model = Products
    form_class = ProductUpdateForm
    template_name = 'userAdmin/products-update-delete.html'
    success_url = reverse_lazy('userAdmin:products_read')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Админ-панель - Редактирование товара'

        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# Отображение и редактирование категорий
class CategoryAdminListView(ListView):
    model = ProductsCategory
    extra_context = {'title': 'Админ-панель - Категории'}
    template_name = ''

    def get_queryset(self):
        return ProductsCategory.objects.all()


class CategoryAdminCreateView(CreateView):
    pass


class CategoryAdminUpdateView(UpdateView):
    pass