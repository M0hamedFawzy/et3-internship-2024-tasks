from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet, DeletedWallets
from SubscriptionPlan.models import SubscriptionPlan
from rest_framework import serializers
from .serializers import WalletSerializer, CreateWalletSerializer, ChargeWalletSerializer, ResetPasswordSerializer, \
    WalletActivationSerializer, WalletDeletionSerializer, RestoreWalletSerialier
from transactions.models import Transaction
from decimal import Decimal


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet_view(request):
    """Retrieve wallet information for the authenticated user."""
    user = request.user

    try:
        # Check if the wallet is in the deleted wallets table
        del_wallet = DeletedWallets.objects.get(user=user)
        if del_wallet.deletion_confirmation:
            return Response({'detail': 'Your wallet is permanently deleted!'}, status=status.HTTP_200_OK)
        else:
            wallet = Wallet.objects.get(user=user)
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    except DeletedWallets.DoesNotExist:
        # If no deleted wallet is found, proceed to check if the user has an active wallet
        try:
            wallet = Wallet.objects.get(user=user)
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({'detail': 'No wallet found. Create one now.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_wallet_view(request):
    """Create a wallet for the authenticated user."""
    user = request.user
    # Check if user already has a wallet
    if Wallet.objects.filter(user=user).exists():
        return Response({'detail': 'Wallet already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CreateWalletSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'Wallet created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def charge_wallet_view(request):
    """Charge the authenticated user's wallet."""
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({'detail': 'No wallet found. Create a wallet first.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Check if the wallet is in the deleted wallets table
        del_wallet = DeletedWallets.objects.get(user=user)
        if del_wallet.deletion_confirmation:
            return Response({'detail': 'Your wallet is permanently deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Your wallet is in the process of deletion. to perform any action restore the wallet within the 3 days'}, status=status.HTTP_200_OK)
    except DeletedWallets.DoesNotExist:
        pass

    if not wallet.is_active:
        return Response({'detail': 'Warning! you need to activate your wallet first to perform any action'})

    serializer = ChargeWalletSerializer(data=request.data, context={'wallet': wallet})
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'success': 'Wallet charged successfully'}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password_view(request):
    """Reset the password for the user with authenticated information"""
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({'detail': 'No wallet found. Create a wallet first.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ResetPasswordSerializer(data=request.data, context={'wallet': wallet})
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'success': 'Wallet Password reset successfully'}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wallet_activation_view(request):
    """Activate of Deactivate the wallet for the user"""
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({'detail': 'No wallet found. Create a wallet first.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = WalletActivationSerializer(data=request.data, context={'wallet': wallet})

    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'success': 'Wallet activation changed successfully'}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restore_wallet_view(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({'detail': 'No wallet found. Create a wallet first.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        del_wallet = DeletedWallets.objects.get(user=user)
    except DeletedWallets.DoesNotExist:
        return Response({'detail': 'your wallet is not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RestoreWalletSerialier(data=request.data, context={'wallet': wallet, 'deleted_wallet': del_wallet})
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'success': 'your wallet Restored Successfully'}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initial_deletion_view(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({'detail': 'No wallet found. Create a wallet first.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = WalletDeletionSerializer(data=request.data, context={'wallet': wallet})

    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'success': 'Wallet is deleted. you can restore your wallet within 3 days, After that your wallet will be deleted permenantly'}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def final_deletion_view(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({'detail': 'No wallet found. Create a wallet first.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        del_wallet = DeletedWallets.objects.get(user=user)
    except DeletedWallets.DoesNotExist:
        return Response({'detail': 'your wallet is not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    msg = wallet.final_deletion(del_wallet)
    return Response({'detail': msg}, status=status.HTTP_200_OK)

