"""This module contains users app all models definitions."""
from django.contrib.auth.models import AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    """Custom user extending default Django user."""
    email = models.EmailField(unique=True)
