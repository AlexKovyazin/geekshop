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

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/add/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login/?next=/basket/add/1/')
        self.assertEqual(response.status_code, 302)

        # с логином все должно быть хорошо
        self.client.login(username='BrotherOfPekMek', password='TestCase145')
        self.assertFalse(response.context['user'].is_anonimous)

        response = self.client.get('/basket/add/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/add/1')
        self.assertIn('Ваша корзина, Пользователь', response.content.decode())

    def tearDown(self):
        call_command('sqlsequencereset', 'products', 'users', 'orders', 'basket')
