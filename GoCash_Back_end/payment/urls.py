from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_portal, name='payment'),
    path('payment-portal/', views.pay, name='payment-portal'),
]
