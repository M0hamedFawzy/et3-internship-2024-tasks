from django.contrib import admin

from .models import SubscriptionPlan


class SubscriptionPlansAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_display_links = ('id', 'name', 'price')


admin.site.register(SubscriptionPlan, SubscriptionPlansAdmin)
