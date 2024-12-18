from rest_framework import serializers
from .models import Wallet, DeletedWallets
from decimal import Decimal
from transactions.models import Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'is_active', 'deleted']  # Include only necessary fields


class CreateWalletSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, max_length=6)
    repass = serializers.CharField(write_only=True, max_length=6)

    def validate_password(self, value):
        """Validate the password."""
        if len(value) < 4:
            raise serializers.ValidationError("Password must be at least 4 digits long.")
        if value == '000000':  # Assuming password shouldn't be all zeros
            raise serializers.ValidationError("Password cannot be all zeros.")
        return value

    def validate(self, data):
        """Ensure that password and repass match."""
        if data['password'] != data['repass']:
            raise serializers.ValidationError({"repass": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """Create a new wallet for the user."""
        user = self.context['request'].user
        password = validated_data['password']
        wallet = Wallet.create_wallet(user=user, password=password)
        return wallet


class ChargeWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.CharField(max_length=50)

    def validate_amount(self, value):
        """Ensure the amount is valid for charging."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        """Charge the wallet and create a transaction."""
        wallet = self.context['wallet']
        amount = validated_data['amount']
        payment_method = validated_data['payment_method']

        # Charge the wallet and create the transaction
        try:
            new_balance = wallet.charge_wallet(
                amount=Decimal(amount),
                payment_method=payment_method,
                transaction_model=Transaction
            )
        except ValueError as e:
            raise serializers.ValidationError({"detail": str(e)})

        return wallet


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, max_length=6)
    new_password = serializers.CharField(write_only=True, max_length=6)

    def validate_old_password(self, value):
        """Ensure the user enters the old password right"""
        wallet_password = self.context['wallet'].wallet_pass
        if value != wallet_password:
            raise serializers.ValidationError('Wrong old password!')
        return value

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError('The New password is the same old password!')
        return data

    def create(self, validated_data):
        wallet = self.context['wallet']
        new_password = validated_data['new_password']

        try:
            wallet.reset_password(new_password)
        except ValueError as e:
            raise serializers.ValidationError({'detail': str(e)})

        return wallet

class WalletActivationSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, max_length=6)
    state = serializers.BooleanField()

    def validate_password(self, value):
        """Ensure the user enters the right password for activation/deactivation action"""
        wallet_pass = self.context['wallet'].wallet_pass
        if value != wallet_pass:
            raise serializers.ValidationError("Wrong Password! Try again")
        return value

    def validate_state(self, value):
        """Ensure that state field is a boolean field"""
        if not isinstance(value, bool):
            raise serializers.ValidationError('Invalid Entry')
        return value

    def create(self, validated_data):
        wallet = self.context['wallet']
        wallet.wallet_activation(validated_data['state'])
        return wallet



class WalletDeletionSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, max_length=6)
    confirm_txt = serializers.CharField(max_length=10)

    def validate_password(self, value):
        """Ensure the user enters the right password for deletion action"""
        wallet_pass = self.context['wallet'].wallet_pass
        if value != wallet_pass:
            raise serializers.ValidationError("Wrong Password! Try again")
        return value

    def validate_confirm_txt(self, value):
        if value == 'I Confirm' or value == 'i confirm':
            return value
        else:
            raise serializers.ValidationError('Wrong Entry! Please type the shown text exactly as shown')

    def create(self, validated_data):
        wallet = self.context['wallet']
        if wallet.balance < Decimal(20):
            raise serializers.ValidationError('You need at least 20 EGP in your balance for deleting your wallet')
        else:
            wallet.initial_deletion(DeletedWallets)
        return wallet


class RestoreWalletSerialier(serializers.Serializer):
    password = serializers.CharField(write_only=True, max_length=6)

    def validate_password(self, value):
        """Ensure the user enters the right password for restoration action"""
        wallet_pass = self.context['wallet'].wallet_pass
        if value != wallet_pass:
            raise serializers.ValidationError("Wrong Password! Try again")
        return value

    def create(self, validated_data):
        wallet = self.context['wallet']
        del_wallet = self.context['deleted_wallet']
        wallet.wallet_restore(del_wallet)

        return wallet
