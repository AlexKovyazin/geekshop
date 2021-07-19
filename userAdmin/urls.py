from django.urls import path
from userAdmin.views import index, UserCreateView, UserListView, UserUpdateView, UserDeleteView

app_name = 'userAdmin'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='read_users'),
    path('users/create/', UserCreateView.as_view(), name='create_user'),
    path('users/update_user/<int:pk>/', UserUpdateView.as_view(), name='update_user'),
    path('users/delete_user/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
]
