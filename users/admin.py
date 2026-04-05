from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_approved', 'is_blocked', 'is_staff']
    list_filter = ['role', 'is_approved', 'is_blocked']
    fieldsets = UserAdmin.fieldsets + (
        ('TaskMates Info', {'fields': ('role', 'is_approved', 'is_blocked', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)
