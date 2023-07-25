from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=150, blank=True)
    email = models.EmailField('email', unique=True)

    def __str__(self):
        return self.username
