from django.core.management.base import BaseCommand

from users.models import User, UserProfile


class Command(BaseCommand):
    help = 'Для каждого пользователя в таблице users создает запись в таблице userprofile'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            user_profile = UserProfile.objects.create(user=user)
            user_profile.save()
