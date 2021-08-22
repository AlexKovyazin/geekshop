import hashlib
import random
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
    def is_activation_key_expired(self):
        return True if now() > self.activation_key_expires else False

    # Из-за False авторизация через соц. сети невозможна
    is_active = models.BooleanField(default=False)

    image = models.ImageField(upload_to='users_images', blank=True)
    activation_key = models.CharField(
        max_length=123,
        default=hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:16]
    )
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48))
    )
