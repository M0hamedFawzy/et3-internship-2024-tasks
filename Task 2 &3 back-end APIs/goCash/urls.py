from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('homePage.urls')),
    path('register/', include('homePage.urls')),
    path('sign_in/', include('homePage.urls')),
    path('users/', include('users.urls')),
    path('wallets/', include('wallets.urls')),
    path('creating_wallet/', include('wallets.urls')),
    path('charge_wallet/', include('wallets.urls')),
    path('enterPass/', include('wallets.urls')),
    path('transactions/', include('transactions.urls')),
    path('send_money/', include('transactions.urls')),
    path('withdrawal/', include('transactions.urls')),
    path('notifications/', include('notifications.urls')),
    path('support_tickets/', include('support_tickets.urls')),
    # path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
