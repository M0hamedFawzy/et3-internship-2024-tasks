from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from dwbi.views import dashboard, generate_chart


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homePage.urls')),
    path('dashboard/', include('users.urls')),
    path('wallets/', include('wallets.urls')),
    path('transactions/', include('transactions.urls')),
    path('notifications/', include('notifications.urls')),
    path('support_tickets/', include('support_tickets.urls')),
    path('payment/', include('payment.urls')),
    path('subscription-portal/', include('SubscriptionPlan.urls')),
    path('green-portal/', include('GreenPlan.urls')),
    path('dwbi_dashboard/', dashboard, name='dwbi_dashboard'),
    path('generate_chart/', generate_chart, name='generate_chart'),
]
