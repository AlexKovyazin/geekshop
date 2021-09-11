import hashlib
import random
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    def is_activation_key_expired(self):
        return True if now() > self.activation_key_expires else False

    is_active = models.BooleanField(default=True)

    image = models.ImageField(upload_to='users_images', blank=True)
    activation_key = models.CharField(
        max_length=123,
        default=hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:16]
    )
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48))
    )


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='тэги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='о себе', max_length=256, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
