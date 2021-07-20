from django.urls import path
from users.views import UserLoginView, UserLogoutView, UserCreateView, profile
# from users.views import UserProfileView

app_name = 'users'

urlpatterns = [
    path('', UserLogoutView.as_view(), name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('profile/', profile, name='profile'),
    # path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
]
