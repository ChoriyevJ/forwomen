from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='users/', blank=True)

    def __str__(self):
        return self.first_name if self.first_name else self.username

    def __repr__(self):
        return f'CustomUser(pk={self.pk}, username="{self.username}")'
