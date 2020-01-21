"""This module contains accounts app url definitions."""
from django.urls import path

from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]
