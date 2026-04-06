from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Avg
from .models import User
from customers.models import Review

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'average_rating', 'is_approved', 'is_blocked', 'is_staff']
    list_filter = ['role', 'is_approved', 'is_blocked']
    fieldsets = UserAdmin.fieldsets + (
        ('TaskMates Info', {'fields': ('role', 'is_approved', 'is_blocked', 'phone_number')}),
    )

    def average_rating(self, obj):
        if obj.role == 'SERVICER':
            avg = Review.objects.filter(service_request__servicer=obj).aggregate(Avg('rating'))['rating__avg']
            if avg is not None:
                return round(avg, 2)
            return "No Ratings"
        return "-"
    average_rating.short_description = 'Avg Rating'

admin.site.register(User, CustomUserAdmin)
