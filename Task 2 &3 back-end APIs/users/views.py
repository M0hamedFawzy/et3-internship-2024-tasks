from django.shortcuts import render, redirect
from django.http import HttpResponse
from wallets.models import Wallet
from django.shortcuts import render, get_object_or_404
from users.models import User
from django.contrib import messages


def index(request):
    phone = request.session.get('phone_number')
    if not phone:
        messages.error(request, "User not logged in.")
        return redirect('sign_up')

    user = get_object_or_404(User, phone_number=phone)
    try:
        wallet = get_object_or_404(Wallet, user=user)
    except:
        wallet = None
    return render(request, 'users/users.html', {'user': user,
                                                'wallet': wallet,
                                                'balance': wallet.balance if wallet else 0})
