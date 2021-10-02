from django.urls import path
from userAdmin.views import index, UserAdminCreateView, UserAdminListView, UserAdminUpdateView, UserAdminDeleteView, \
    ProductsAdminListView, ProductsAdminCreateView, ProductsAdminUpdateView, CategoryAdminUpdateView, \
    CategoryAdminCreateView, CategoryAdminListView, ProductsAdminDeleteView, CategoryAdminDeleteView, \
    OrdersAdminListView, OrdersAdminCreateView, OrdersAdminUpdateView, OrdersAdminDeleteView

app_name = 'userAdmin'

urlpatterns = [
    path('', index, name='index'),

    path('orders/', OrdersAdminListView.as_view(), name='orders_read'),
    path('orders/create/', OrdersAdminCreateView.as_view(), name='orders_create'),
    path('orders/update_order/<int:pk>/', OrdersAdminUpdateView.as_view(), name='orders_update'),
    path('orders/delete_order/<int:pk>/', OrdersAdminDeleteView.as_view(), name='orders_delete'),

    path('users/', UserAdminListView.as_view(), name='users_read'),
    path('users/create/', UserAdminCreateView.as_view(), name='create_user'),
    path('users/update_user/<int:pk>/', UserAdminUpdateView.as_view(), name='update_user'),
    path('users/delete_user/<int:pk>/', UserAdminDeleteView.as_view(), name='delete_user'),

    path('products/', ProductsAdminListView.as_view(), name='products_read'),
    path('products/create/', ProductsAdminCreateView.as_view(), name='products_create'),
    path('products/update/<int:pk>/', ProductsAdminUpdateView.as_view(), name='products_update'),
    path('products/delete/<int:pk>/', ProductsAdminDeleteView.as_view(), name='products_delete'),

    path('category/', CategoryAdminListView.as_view(), name='category_read'),
    path('category/create/', CategoryAdminCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryAdminUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryAdminDeleteView.as_view(), name='category_delete'),
]
