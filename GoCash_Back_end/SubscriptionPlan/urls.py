from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscribe_portal, name='subscription-portal'),
    path('subscribe/', views.subscribe_action, name='subscribe'),
]
