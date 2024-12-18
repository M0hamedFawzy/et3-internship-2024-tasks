from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet_view, name='wallets'),
    path('creating_wallet/', views.create_wallet_view, name='creating_wallet'),
    path('charge_wallet/', views.charge_wallet_view, name='charge_wallet'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('restore_wallet/', views.restore_wallet_view, name='restore_wallet'),
    path('wallet_activation/', views.wallet_activation_view, name='wallet_activation'),
    path('initial_delete/', views.initial_deletion_view, name='initial_delete'),
    path('final_delete/', views.final_deletion_view, name='final_delete'),
]
