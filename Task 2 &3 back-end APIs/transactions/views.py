from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from users.models import User
from transactions.models import Transaction
from wallets.models import Wallet
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.db.models import Q


def transaction(request):
    phone = request.session.get('phone_number')
    if not phone:
        messages.error(request, "User not logged in.")
        return redirect('sign_up')
    user = get_object_or_404(User, phone_number=phone)
    try:
        wallet = get_object_or_404(Wallet, user=user)
        transactions = Transaction.objects.filter(
            Q(sender=user, user_wallet=wallet) | Q(receiver=user.phone_number, service_type="Transaction", user_wallet=wallet)
        )
    except:
        transactions = None

    return render(request, 'transactions/transactions.html', {
        'transactions': transactions
    })


def send_money(request):
    if request.method == 'POST':
        phone = request.session.get('phone_number')
        if not phone:
            messages.error(request, "User not logged in.")
            return redirect('sign_up')

        user = get_object_or_404(User, phone_number=phone)
        try:
            wallet = get_object_or_404(Wallet, user=user)
        except:
            wallet = None
            messages.error(request, "Create wallet first to make transactions!")
            return redirect('/transactions/send_money')


        reciever_number = request.POST.get('reciever_number')
        if reciever_number == user.phone_number:
            messages.error(request, "You can't make a transaction to yourself!")
            return redirect('/transactions/send_money')

        amount = Decimal(request.POST.get('amount'))
        if amount > Decimal(wallet.balance) or amount <= 0:
            messages.error(request, 'Insufficient funds! Please enter a valid amount.')
            return render(request, 'transactions/send_money.html')

        try:
            rec_user = get_object_or_404(User, phone_number=reciever_number)
        except:
            rec_user = None

        message = Transaction.process_send_money(user, rec_user, reciever_number, wallet, amount)
        messages.success(request, message)
        return redirect('/transactions/send_money')

    return render(request, 'transactions/send_money.html')


def withdrawal(request):
    if request.method == 'POST':
        phone = request.session.get('phone_number')
        if not phone:
            messages.error(request, "User not logged in.")
            return redirect('sign_up')

        user = get_object_or_404(User, phone_number=phone)

        try:
            wallet = get_object_or_404(Wallet, user=user)
        except:
            wallet = None
            messages.error(request, "Create wallet first to make transactions!")
            return redirect('/transactions/withdrawal')

        amount = Decimal(request.POST.get('amount'))
        method = request.POST.get('payment_method')

        if amount > wallet.balance or amount <= 0:
            messages.error(request, 'Insufficient funds! Please enter a valid amount.')
            return render(request, 'transactions/withdrawal.html')

        message = Transaction.process_withdrawal(user, wallet, amount, method)
        messages.success(request, f'Withdrawal completed successfully.\n{message}')
        return redirect('/transactions/withdrawal')

    return render(request, 'transactions/withdrawal.html')




