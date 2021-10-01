from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

from users.models import User, UserProfile
from datetime import timedelta


class TestProductsSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_activation_key_expired(self):
        self.user = User.objects.create_user(username='PekMek',
                                             email='PekMek@gmail.com',
                                             password='TestCase144')

        self.assertFalse(self.user.is_activation_key_expired())
        self.user.activation_key_expires -= timedelta(days=3)
        self.assertTrue(self.user.is_activation_key_expired())

    def test_create_user_profile(self):
        num_of_profiles_before = len(UserProfile.objects.all())

        self.user = User.objects.create_user(username='PekMek',
                                             email='PekMek@gmail.com',
                                             password='TestCase144')

        num_of_profiles_after = len(UserProfile.objects.all())

        self.assertGreater(num_of_profiles_after, num_of_profiles_before)
