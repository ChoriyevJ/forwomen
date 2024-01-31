from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        modul = CustomUser
        fields = ('username', 'email', 'photo',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        modul = CustomUser
        fields = ('email', 'first_name', 'last_name', 'photo',)

