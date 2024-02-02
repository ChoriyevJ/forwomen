from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('pk', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_editable = ('is_active', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('photo', )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('photo', )}),
    )

    actions = ['show_passwords']



