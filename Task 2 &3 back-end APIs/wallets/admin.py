from django.contrib import admin

from .models import Wallet


class WalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_id', 'user_id', 'wallet_pass', 'balance')
    list_display_links = ('wallet_id', 'user_id')
    search_fields = ('wallet_id', 'user_id')
    list_per_page = 25


admin.site.register(Wallet, WalletAdmin)
