from django.test import TestCase
from django.test.client import Client
from users.models import User
from django.core.management import call_command


class TestUserManagement(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = User.objects.create_superuser(
            username='SuperDuper',
            email='SuperDuper@gmail.com',
            password='TestCase143')

        self.user = User.objects.create_user(username='PekMek',
                                             email='PekMek@gmail.com',
                                             password='TestCase144')

        self.user_with__first_name = User.objects.create_user(username='BrotherOfPekMek',
                                                              email='BrPekMek@gmail.com',
                                                              password='TestCase145')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'GeekShop')
        self.assertNotContains(response, 'Профиль', status_code=200)

        # данные пользователя
        self.client.login(username='PekMek', password='TestCase144')

        # логинимся
        response = self.client.get('/users/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Профиль', status_code=200)
        self.assertEqual(response.context['user'], self.user)

    def test_user_logout(self):
        # главная до авторизации
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        # логинимся
        self.client.login(username='BrotherOfPekMek', password='TestCase145')
        # главная после авторизации
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # выходим из системы
        self.client.logout()

        # главная после выхода
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def tearDown(self):
        call_command('sqlsequencereset', 'products', 'users', 'orders', 'basket')
