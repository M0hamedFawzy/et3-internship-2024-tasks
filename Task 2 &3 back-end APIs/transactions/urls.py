from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction, name='transactions'),
    path('send_money/', views.send_money, name='send_money'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
]