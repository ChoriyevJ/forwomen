from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        abstract = True






