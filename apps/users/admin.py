"""This module contains users app admin page definition."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Represents users management module of admin page."""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ('username',)
    search_fields = ('username',)
    list_display = ['username', 'email', 'is_staff']
    readonly_fields = [
        'first_name',
        'last_name',
        'password',
        'date_joined',
    ]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Returns user creation form available only for superuser."""
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['username'].disabled = True

        return form


admin.site.register(CustomUser, CustomUserAdmin)
