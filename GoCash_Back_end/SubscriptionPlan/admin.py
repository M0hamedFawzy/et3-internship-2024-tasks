from django.contrib import admin
from .models import SubscriptionPlan, PlanSubscribedUsers


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'max_balance', 'max_transactions')
    list_display_links = ('id', 'name', 'price', 'max_balance', 'max_transactions')
    search_fields = ('id', 'name', 'price', 'max_balance', 'max_transactions')


class PlanSubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan_id', 'user_phone_number', 'subscription_start_date', 'subscription_end_date')
    list_display_links = ('id', 'plan_id', 'user_phone_number')
    search_fields = ('plan_id', 'user_phone_number', 'subscription_start_date', 'subscription_end_date')


admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(PlanSubscribedUsers, PlanSubscribedUsersAdmin)
