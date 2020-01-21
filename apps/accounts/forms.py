"""This module contains UserRegisterForm class extending default registration form."""
from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import CustomUser


class UserRegisterForm(UserCreationForm):
    """Extends default registration form by adding email required to sing up."""
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
