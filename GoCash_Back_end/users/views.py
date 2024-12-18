from django.shortcuts import render, redirect
from django.http import HttpResponse
from wallets.models import Wallet, DeletedWallets
from django.shortcuts import render, get_object_or_404
from users.models import User
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDashboard(request):
    if request.method == 'GET':
        user = request.user

        try:
            del_wallet = DeletedWallets.objects.get(user=user)
            if del_wallet.deletion_confirmation:
                msg_2 = 'Wallet deleted permanently'
                wallet = None
                msg_3 = 'no info'
            else:
                msg_2 = 'Wallet is in the process of deletion'
                wallet = None
                msg_3 = 'no info'
        except DeletedWallets.DoesNotExist:
            try:
                wallet = Wallet.objects.get(user=user)
                msg_1 = f'{wallet.balance} EGP'
            except Wallet.DoesNotExist:
                wallet = None
                msg_2 = 'Create a Wallet now :)'
                msg_3 = 'no info'

        data = {
            'username': user.username,
            'PhoneNumber': user.phone_number,
            'SubscriptionPlan': f'{user.subscription_plan.name} Plan {user.subscription_plan.price}EGP / Month',
            'Balance': f'{msg_1 if wallet else msg_2}',
            'Status': f'{wallet.is_active if wallet else msg_3}',
        }

        return Response(data, status=status.HTTP_200_OK)

    return Response({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
