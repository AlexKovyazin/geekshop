from django.urls import path
from userAdmin.views import index, UserAdminCreateView, UserAdminListView, UserAdminUpdateView, UserAdminDeleteView
from orders.views import AdminOrdersList

app_name = 'userAdmin'

urlpatterns = [
    path('', index, name='index'),
    path('orders/', AdminOrdersList.as_view(), name='AdminOrdersList'),
    path('users/', UserAdminListView.as_view(), name='read_users'),
    path('users/create/', UserAdminCreateView.as_view(), name='create_user'),
    path('users/update_user/<int:pk>/', UserAdminUpdateView.as_view(), name='update_user'),
    path('users/delete_user/<int:pk>/', UserAdminDeleteView.as_view(), name='delete_user'),

]
