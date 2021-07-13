from django.shortcuts import render


def index(request):
    return render(request, 'userAdmin/index.html')


def create_user(request):
    return render(request, 'userAdmin/userAdmin-create.html')


def read_users(request):
    return render(request, 'userAdmin/userAdmin-read.html')


def update_user(request):
    pass


def delete_user(request):
    pass
