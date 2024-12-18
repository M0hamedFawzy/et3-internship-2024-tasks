from django.contrib import admin
from .models import GreenPlan, GreenSubscribedUsers


class GreenPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'green_type', 'price')
    list_display_links = ('id', 'green_type', 'price')
    search_fields = ('id', 'green_type', 'price')


class GreenSubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'g_type_id', 'user_phone_number', 'subscription_start_date', 'subscription_end_date')
    list_display_links = ('id', 'g_type_id', 'user_phone_number')
    search_fields = ('g_type_id', 'user_phone_number', 'subscription_start_date', 'subscription_end_date')


admin.site.register(GreenPlan, GreenPlanAdmin)
admin.site.register(GreenSubscribedUsers, GreenSubscribedUsersAdmin)
