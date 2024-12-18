from django.urls import path
from . import views

urlpatterns = [
    path('', views.green_portal, name='green-portal'),
    path('subscribe/', views.green_subscribe_action, name='green-subscribe'),
]
