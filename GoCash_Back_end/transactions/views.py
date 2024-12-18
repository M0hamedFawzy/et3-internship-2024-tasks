from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer, SendMoneySerializer, WithdrawalSerializer
from wallets.models import Wallet, DeletedWallets
from users.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from decimal import Decimal
from django.db import transaction as db_transaction


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_list(request):
    """
    List all transactions related to the authenticated user.
    """
    user = request.user

    try:
        # Check if the wallet is in the deleted wallets table
        del_wallet = DeletedWallets.objects.get(user=user)
        if del_wallet.deletion_confirmation:
            return Response({'detail': 'Your wallet is permanently deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Your wallet is in the process of deletion. to perform any action restore the wallet within the 3 days'}, status=status.HTTP_200_OK)
    except DeletedWallets.DoesNotExist:
        # If no deleted wallet is found, proceed to check if the user has an active wallet
        try:
            wallet = Wallet.objects.get(user=user)
            transactions = Transaction.objects.filter(
                Q(sender=user, user_wallet=wallet) |
                Q(receiver=user.phone_number, service_type="Transaction", user_wallet=wallet)
            ).order_by('-transaction_date')
        except Wallet.DoesNotExist:
            return Response({'detail': 'Your wallet not created yet!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_money(request):
    """
    Handle sending money from the authenticated user to another user.
    """
    user = request.user
    try:
        # Check if the wallet is in the deleted wallets table
        del_wallet = DeletedWallets.objects.get(user=user)
        if del_wallet.deletion_confirmation:
            return Response({'detail': 'Your wallet is permanently deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Your wallet is in the process of deletion. to perform any action restore the wallet within the 3 days'}, status=status.HTTP_200_OK)
    except DeletedWallets.DoesNotExist:
        pass

    serializer = SendMoneySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        rec_number = serializer.validated_data['reciever_number']
        amount = serializer.validated_data['amount']
        user = request.user

        try:
            rec_user = User.objects.get(phone_number=rec_number)
        except User.DoesNotExist:
            rec_user = None

        try:
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            return Response({"detail": "Wallet does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if not wallet.is_active:
            return Response({'detail': 'Warning! you need to activate your wallet first to perform any action'})

        try:
            with db_transaction.atomic():
                message = Transaction.process_send_money(user, rec_user, rec_number, wallet, amount)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": message}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdrawal(request):
    """
    Handle withdrawal operations for the authenticated user.
    """
    user = request.user
    try:
        # Check if the wallet is in the deleted wallets table
        del_wallet = DeletedWallets.objects.get(user=user)
        if del_wallet.deletion_confirmation:
            return Response({'detail': 'Your wallet is permanently deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Your wallet is in the process of deletion. to perform any action restore the wallet within the 3 days'}, status=status.HTTP_200_OK)
    except DeletedWallets.DoesNotExist:
        pass

    serializer = WithdrawalSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        amount = serializer.validated_data['amount']
        method = serializer.validated_data['payment_method']
        user = request.user

        try:
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            return Response({"detail": "Wallet does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if not wallet.is_active:
            return Response({'detail': 'Warning! you need to activate your wallet first to perform any action'})

        try:
            with db_transaction.atomic():
                message = Transaction.process_withdrawal(user, wallet, amount, method)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": f'Withdrawal completed successfully.\n{message}'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
