from django.shortcuts import render

from users.models import User


def index(request):
    return render(request, 'userAdmin/index.html')


def create_user(request):
    return render(request, 'userAdmin/userAdmin-create.html')


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
