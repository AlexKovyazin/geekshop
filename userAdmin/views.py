from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import User
from userAdmin.forms import AdminUserRegistrationForm, AdminUserUpdateForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    return render(request, 'userAdmin/index.html')


class UserListView(ListView):
    model = User
    template_name = 'userAdmin/userAdmin-read.html'


class UserCreateView(CreateView):
    model = User
    form_class = AdminUserRegistrationForm
    template_name = 'userAdmin/userAdmin-create.html'
    success_url = reverse_lazy('userAdmin:read_users')


class UserUpdateView(UpdateView):
    model = User
    form_class = AdminUserUpdateForm
    template_name = 'userAdmin/userAdmin-update-delete.html'
    success_url = reverse_lazy('userAdmin:read_users')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'userAdmin/userAdmin-update-delete.html'
    success_url = reverse_lazy('userAdmin:read_users')


# @user_passes_test(lambda u: u.is_staff)
# def create_user(request):
#     if request.method == 'POST':
#         form = AdminUserRegistrationForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('userAdmin:read_users'))
#
#     else:
#         form = AdminUserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'userAdmin/userAdmin-create.html', context)


# @user_passes_test(lambda u: u.is_staff)
# def read_users(request):
#     users = User.objects.all()
#     context = {
#         'users': users
#     }
#     return render(request, 'userAdmin/userAdmin-read.html', context)


# @user_passes_test(lambda u: u.is_staff)
# def update_user(request, user_id):
#     selected_user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = AdminUserUpdateForm(instance=selected_user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             print('форма сохранена')
#             return HttpResponseRedirect(reverse('userAdmin:read_users'))
#     else:
#         form = AdminUserUpdateForm(instance=selected_user)
#     context = {
#         'selected_user': selected_user,
#         'form': form
#     }
#     return render(request, 'userAdmin/userAdmin-update-delete.html', context)


# @user_passes_test(lambda u: u.is_staff)
# def delete_user(request, user_id):
#     selected_user = User.objects.get(id=user_id)
#     selected_user.is_active = False
#     selected_user.save()
#     return HttpResponseRedirect(reverse('userAdmin:read_users'))
