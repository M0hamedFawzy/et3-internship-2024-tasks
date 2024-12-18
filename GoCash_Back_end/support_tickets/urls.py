from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='support_tickets')
]