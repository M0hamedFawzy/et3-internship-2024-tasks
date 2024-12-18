from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import User
from SubscriptionPlan.models import SubscriptionPlan
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def home_page(request):
    return render(request, 'homePage/home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone')

        if not username or not phone_number:
            messages.error(request, 'Both username and phone number are required.')
            return render(request, 'homePage/register.html')

        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number is already registered.')
            return render(request, 'homePage/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'homePage/register.html')

        try:
            default_plan = SubscriptionPlan.objects.get(id=1)
        except SubscriptionPlan.DoesNotExist:
            messages.error(request, 'Default subscription plan not found.')
            return render(request, 'homePage/register.html')

        new_user = User(username=username, phone_number=phone_number, subscription_plan=default_plan)
        new_user.save()

        messages.success(request, 'Registration successful! Now you can sign in.')
        return redirect('/sign_in')

    return render(request, 'homePage/register.html')


def sign_in(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')

        if not phone:
            messages.error(request, 'phone number is required.')
            return render(request, 'homePage/signin.html')
        try:
            user = User.objects.get(phone_number=phone)
            request.session['phone_number'] = phone
            return redirect('users')
        except User.DoesNotExist:
            messages.error(request, "User doesn't have an account. Please register first.")
            return redirect('sign_in')
    return render(request, 'homePage/signin.html')
