from django.urls import path
from users.views import login, registration, logout, profile

app_name = 'users'

urlpatterns = [
    path('', logout, name='logout'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
]
