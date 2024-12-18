from django.utils import timezone
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
from .models import GreenPlan
from .serializers import GreenPlanSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def green_portal(request):
    user = request.user
    green_id = user.green_user_status_id

    if green_id is None:
        user_green_plan = 'User Not Registered in Green Plan'
    else:
        user_green_plan = user.green_user_status.green_type

    all_plans = GreenPlan.objects.all()
    all_green_plans = [
        {
            "name": plan.green_type,
            "price_per_month": plan.price
        }
        for plan in all_plans
    ]

    data = {
        "user-green-subscription-name": user_green_plan,
        "all-subscription-plans": all_green_plans
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def green_subscribe_action(request):
    user = request.user

    try:
        # Check if the wallet is in the deleted wallets table
        del_wallet = DeletedWallets.objects.get(user=user)
        if del_wallet.deletion_confirmation:
            return Response({'detail': 'Your wallet is permanently deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({
                                'detail': 'Your wallet is in the process of deletion. to perform any action restore the wallet within the 3 days'},
                            status=status.HTTP_200_OK)
    except DeletedWallets.DoesNotExist:
        pass

    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({"detail": "Wallet does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    if not wallet.is_active:
        return Response({'detail': 'Warning! you need to activate your wallet first to perform any action'})

    serializer = GreenPlanSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        plan_name = serializer.validated_data['plan_name']
        user = request.user
        green_plan = GreenPlan.objects.get(green_type=plan_name)
        sub_start_date = timezone.now()

        try:
            with db_transaction.atomic():
                message = Transaction.process_green_subscribe(
                    user=user,
                    wallet=wallet,
                    g_plan=green_plan,
                    sub_start_date=sub_start_date
                )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": f'{message}'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

