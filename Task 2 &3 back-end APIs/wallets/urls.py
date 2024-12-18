from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet, name='wallets'),
    path('creating_wallet/', views.create_wallet, name='creating_wallet'),
    path('charge_wallet/', views.charge_wallet, name='charge_wallet'),
    path('enterPass/', views.password_check, name='enterPass')
]
