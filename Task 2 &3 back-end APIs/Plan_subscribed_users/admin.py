from django.contrib import admin

from .models import Plan_subscribed_users

class psAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan_id', 'user_id', 'subscription_start_date', 'subscription_end_date')


admin.site.register(Plan_subscribed_users, psAdmin)
