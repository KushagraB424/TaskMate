from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.role == 'SERVICER':
            user.is_approved = False # Require admin approval
        if commit:
            user.save()
        return user
