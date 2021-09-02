from django import forms

from basket.models import Basket
from orders.models import Order, OrderItem
from products.models import Products


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields['product'].queryset = Products.get_items()
            field.widget.attrs['class'] = 'form-control'

    # Очищает корзину пльзователя при сохранении формы заказа
    # def save(self, commit=True):
    #     instance = super(OrderItemForm, self).save(commit=False)
    #     basket_items = Basket.objects.filter(user=self.user)
    #     if commit:
    #         basket_items.delete()
    #     return instance
