from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from unicodedata import decimal
from users.models import User
from wallets.models import Wallet
from transactions.models import Transaction
from django.contrib import messages
from decimal import Decimal, InvalidOperation


def wallet(request):
    phone = request.session.get('phone_number')
    if not phone:
        messages.error(request, "User not logged in.")
        return redirect('sign_up')
    user = get_object_or_404(User, phone_number=phone)
    try:
        wallet = get_object_or_404(Wallet, user=user)
    except:
        wallet = None
    return render(request, 'wallets/wallets.html', {
        'wallet': wallet,
    })


def password_check(request):
    if request.method == 'POST':
        phone = request.session.get('phone_number')
        if not phone:
            messages.error(request, "User not logged in.")
            return redirect('sign_up')

        user = get_object_or_404(User, phone_number=phone)
        wallet = get_object_or_404(Wallet, user=user)

        entered_pass = str(request.POST.get('password'))

        if wallet.check_password(entered_pass):
            return redirect('/wallets/charge_wallet')
        else:
            messages.error(request, 'Wrong Password')

    return render(request, 'wallets/password_first.html')


def create_wallet(request):
    if request.method == 'POST':
        password = str(request.POST.get('password'))
        repass = str(request.POST.get('repassword'))

        if len(password) < 4:
            messages.error(request, 'password must be at least 4 Numbers! Try again')
            return render(request, 'wallets/creating_wallet.html')

        if len(password) == 0:
            messages.error(request, 'password must not be zeros! Try again')
            return render(request, 'wallets/creating_wallet.html')

        if not password == repass:
            messages.error(request, 'Passwords do not match')
            return render(request, 'wallets/creating_wallet.html')

        phone = request.session.get('phone_number')
        if not phone:
            messages.error(request, "User not logged in.")
            return redirect('sign_up')

        user = get_object_or_404(User, phone_number=phone)

        Wallet.create_wallet(user=user, password=password)
        messages.success(request, 'your wallet has been created')
        return redirect('/wallets')

    return render(request, 'wallets/creating_wallet.html')


def charge_wallet(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')

        try:
            amount = Decimal(amount)
        except InvalidOperation:
            messages.error(request, 'Invalid amount entered! Try again.')
            return render(request, 'wallets/charge_wallet.html')

        phone = request.session.get('phone_number')
        if not phone:
            messages.error(request, "User not logged in.")
            return redirect('sign_up')

        user = get_object_or_404(User, phone_number=phone)
        wallet = get_object_or_404(Wallet, user=user)

        try:
            wallet.charge_wallet(amount=amount, payment_method=payment_method, transaction_model=Transaction)
            messages.success(request, 'Wallet charged successfully!')
            return redirect('/wallets')
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'wallets/charge_wallet.html')

    return render(request, 'wallets/charge_wallet.html')


