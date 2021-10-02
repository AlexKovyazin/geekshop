from django import forms
from django.views.generic import UpdateView

from orders.models import Order
from products.models import Products, ProductsCategory
from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User


# Формы пользователей
class AdminUserRegistrationForm(UserRegistrationForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
    }), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image')


class AdminUserUpdateForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4'}))


# Формы товаров
class ProductCreateForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'Активный'),
        (False, 'Неактивный')
    )

    is_active = forms.ChoiceField(
        choices=TRUE_FALSE_CHOICES,
        widget=forms.Select(),
        required=True)

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
    }), required=False)

    class Meta:
        model = Products
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductUpdateForm(ProductCreateForm):
    """
    В процессе переработки форма полностью унаследовалась от ProductCreateForm.
    Название оставлено во views.py для понимания логики
    """
    pass


# Формы категорий
class CategoryCreateForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'Активный'),
        (False, 'Неактивный')
    )

    is_active = forms.ChoiceField(
        choices=TRUE_FALSE_CHOICES,
        widget=forms.Select(),
        required=True)

    class Meta:
        model = ProductsCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CategoryUpdateForm(CategoryCreateForm):
    """
    Название используется во views.py для понимания логики
    """
    discount = forms.IntegerField(
        label='скидка',
        required=False,
        min_value=0,
        max_value=90,
        initial=0)


# Формы заказов
class OrdersCreateForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'Активный'),
        (False, 'Неактивный')
    )

    is_active = forms.ChoiceField(
        choices=TRUE_FALSE_CHOICES,
        widget=forms.Select(),
        required=True)

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrdersCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrdersUpdateForm(OrdersCreateForm):
    """
    Название используется во views.py для понимания логики
    """
