from django.contrib import admin
from apps.user.models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',
                    'is_staff')
