from django.contrib import admin

from .models import Green_subscribed_users

class gsAdmin(admin.ModelAdmin):
    list_display = ('id', 'g_type_id', 'user_id', 'subscription_start_date', 'subscription_end_date')


admin.site.register(Green_subscribed_users, gsAdmin)
