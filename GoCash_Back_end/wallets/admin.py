from django.contrib import admin

from .models import Wallet, DeletedWallets


class WalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_id', 'user_id', 'wallet_pass', 'balance', 'is_active', 'deleted')
    list_display_links = ('wallet_id', 'user_id', 'balance', 'wallet_pass')
    search_fields = ('wallet_id', 'user_id')
    list_per_page = 25


class DeletedWalletsAdmin(admin.ModelAdmin):
    list_display = ('wallet_id', 'user_id', 'balance', 'initial_deletion_date', 'final_deletion_date')
    list_display_links = ('wallet_id', 'user_id')
    search_fields = ('wallet_id', 'user_id', 'initial_deletion_date', 'final_deletion_date')
    list_per_page = 25


admin.site.register(Wallet, WalletAdmin)

admin.site.register(DeletedWallets, DeletedWalletsAdmin)
