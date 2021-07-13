from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from users.models import User
from users.forms import UserRegistrationForm


def index(request):
    return render(request, 'userAdmin/index.html')


def create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('userAdmin:read_users'))
        else:
            print(form.errors)

    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'userAdmin/userAdmin-create.html', context)


def read_users(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'userAdmin/userAdmin-read.html', context)


def update_user(request):
    pass


def delete_user(request):
    pass
