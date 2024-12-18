from django.contrib import admin
from django.shortcuts import get_object_or_404
from users.models import User
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    # Custom method to display the sender's phone number
    def sender_phone(self, obj):
        return obj.sender.phone_number

    # Rename the column header in the admin display
    sender_phone.short_description = 'Sender'
    list_display = ('transaction_id', 'sender_id', 'sender_phone', 'receiver', 'service_name', 'service_type', 'amount', 'fees', 'balance_before', 'balance_after', 'transaction_date')
    list_display_links = ('transaction_id', 'sender_id', 'sender_phone', 'service_type', 'service_name', 'amount')
    search_fields = ('transaction_id', 'sender_id', 'service_type')
    list_filter = ('service_type',)
    list_per_page = 25


admin.site.register(Transaction, TransactionAdmin)
