from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transactions.models import Transaction
from wallets.models import Wallet, DeletedWallets
from users.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from decimal import Decimal
from django.db import transaction as db_transaction
from .serializers import PaymentSerializer

leaf_discount = 0.025
tree_discount = 0.05
forest_discount = 0.15


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_portal(request):
    user = request.user
    data = {
        "username": user.username,
        "green-user-status": user.green_user_status_id
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay(request):
    """
    Perform Payment action [Bills - Mobile Charges - Utilities]
    :param request: amount
    :return: Action done successfully - Error in process
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

    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({"detail": "Wallet does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    if not wallet.is_active:
        return Response({'detail': 'Warning! you need to activate your wallet first to perform any action'})

    serializer = PaymentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        amount = serializer.validated_data['amount']
        service_type = serializer.validated_data['service_type']
        service_name = serializer.validated_data['service_name']
        user = request.user

        # Handle Green user discount
        if user.green_user_status_id in [1, 2, 3] and service_type.lower() == 'merchant payment':
            if user.green_user_status_id == 1:
                amount = amount - (amount * Decimal(leaf_discount))
            if user.green_user_status_id == 2:
                amount = amount - (amount * Decimal(tree_discount))
            if user.green_user_status_id == 3:
                amount = amount - (amount * Decimal(forest_discount))

        try:
            with db_transaction.atomic():
                message = Transaction.process_pay(user=user, wallet=wallet, amount=amount, service_type=service_type, service_name=service_name)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": f'Payment Done. \n {message}'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

