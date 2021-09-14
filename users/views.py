from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserProfileFormExtended
from basket.models import Basket
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = UserLoginForm
    extra_context = {'title': 'GeekShop - Авторизация'}


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context


class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass


# class UserProfileView(SuccessMessageMixin, UpdateView):
#     model = User
#     form_class = UserProfileForm
#     template_name = 'users/profile.html'
#     success_url = reverse_lazy('users/profile.html')
#     success_message = 'Данные успешно обновлены'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=None, **kwargs)
#         context['title'] = 'GeekShop - Личный кабинет'
#         context['basket'] = Basket.objects.filter(user_id=self.kwargs['pk'])
#         return context


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, files=request.FILES, data=request.POST)
        form_extended = UserProfileFormExtended(instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные form успешно обновлены')

        # Форма не проходит валидацию!
        if form_extended.is_valid():
            form_extended.save()
            messages.success(request, 'Данные form_extended успешно обновлены')
    else:
        form = UserProfileForm(instance=request.user)
        form_extended = UserProfileFormExtended(instance=request.user.userprofile)
    context = {
        'title': 'GeekShop - Личный кабинет',
        'form': form,
        'form_extended': form_extended,
        # 'basket': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context)


def verify(request, email, activation_key):
    user = User.objects.get(email=email)
    error_message = ''

    try:
        if user.activation_key == activation_key and user.is_activation_key_expired() is False:
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        elif user.activation_key != activation_key:
            error_message = 'Ключ активации указан неверно'
        elif user.is_activation_key_expired():
            error_message = 'Время действия ключа активации истекло'

        return render(request, 'users/verification.html', context={'error_message': error_message})
    except Exception as err:
        print(f'Error activation user: {err.args}')
        return HttpResponseRedirect(reverse('index'))
