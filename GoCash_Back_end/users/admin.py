from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django import forms


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'phone_number', 'is_staff', 'is_superuser', 'is_active', 'subscription_plan', 'green_user_status')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'subscription_plan', 'green_user_status')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Subscriptions', {'fields': ('subscription_plan', 'green_user_status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('phone_number', 'username')
    ordering = ('phone_number',)
    filter_horizontal = ('groups', 'user_permissions',)
    list_per_page = 25


admin.site.register(User, UserAdmin)


