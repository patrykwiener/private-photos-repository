"""This module contains users app forms definitions."""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Extends default user registration form by adding email field."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    """Extends default reset password form by adding email field."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
