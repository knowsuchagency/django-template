from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
