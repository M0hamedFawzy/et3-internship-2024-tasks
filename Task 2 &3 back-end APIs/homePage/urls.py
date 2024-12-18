from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_pg'),
    path('register/', views.register, name='register'),
    path('sign_in/', views.sign_in, name='sign_in')
]
