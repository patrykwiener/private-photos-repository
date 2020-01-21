"""This module contains all class based views for accounts app."""
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.accounts.forms import UserRegisterForm


class SignUp(CreateView):
    """Represents user registration view."""
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
