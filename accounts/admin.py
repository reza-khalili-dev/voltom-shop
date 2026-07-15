from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اضافی', {'fields': ('phone', 'address', 'is_admin_user')}),
    )
    list_display = ['username', 'email', 'phone', 'is_admin_user', 'is_staff']