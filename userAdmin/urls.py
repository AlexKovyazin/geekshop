from django.urls import path
from userAdmin.views import index, UserAdminCreateView, UserAdminListView, UserAdminUpdateView, UserAdminDeleteView, \
    ProductsAdminListView, ProductsAdminCreateView, ProductsAdminUpdateView
from orders.views import AdminOrdersList

app_name = 'userAdmin'

urlpatterns = [
    path('', index, name='index'),

    path('orders/', AdminOrdersList.as_view(), name='AdminOrdersList'),

    path('users/', UserAdminListView.as_view(), name='users_read'),
    path('users/create/', UserAdminCreateView.as_view(), name='create_user'),
    path('users/update_user/<int:pk>/', UserAdminUpdateView.as_view(), name='update_user'),
    path('users/delete_user/<int:pk>/', UserAdminDeleteView.as_view(), name='delete_user'),

    path('products/', ProductsAdminListView.as_view(), name='products_read'),
    path('products/create/', ProductsAdminCreateView.as_view(), name='products_create'),
    path('products/update/<int:pk>/', ProductsAdminUpdateView.as_view(), name='products_update'),
]
