from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
