from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'phone_number', 'registration_date')
    list_display_links = ('user_id', 'username')
    search_fields = ('user_id', 'username', 'phone_number')
    list_per_page = 25


admin.site.register(User, UserAdmin)
