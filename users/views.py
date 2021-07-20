from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
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
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно обновлены')
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': 'GeekShop - Личный кабинет',
        'form': form,
        'basket': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context)
