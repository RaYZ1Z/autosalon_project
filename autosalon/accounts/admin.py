# accounts/admin.py - ПРОСТОЙ ВАРИАНТ
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Добавляем только нужные поля
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone_number', 'role', 'profile_picture', 'department', 'position')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone_number', 'role', 'email', 'department', 'position')
        }),
    )
    list_display = UserAdmin.list_display + ('phone_number', 'role', 'registration_date')
    readonly_fields = ('registration_date', 'date_joined', 'last_login')

admin.site.register(CustomUser, CustomUserAdmin)