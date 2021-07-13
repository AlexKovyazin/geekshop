from django.urls import path
from userAdmin.views import index, create_user, read_users, update_user, delete_user

app_name = 'userAdmin'

urlpatterns = [
    path('', index, name='index'),
    path('users', read_users, name='index'),
    path('create-user', create_user, name='create_user'),
    path('read_users', read_users, name='read_users'),
    path('update_user', update_user, name='update_user'),
    path('delete_user', delete_user, name='delete_user'),
]
