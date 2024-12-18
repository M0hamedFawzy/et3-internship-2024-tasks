from rest_framework import serializers
from .models import Transaction
from wallets.models import Wallet
from decimal import Decimal


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()  # Custom field for sender's phone number

    class Meta:
        model = Transaction
        # Explicitly list the fields to include, excluding 'transaction_id'
        fields = [
            'sender',
            'receiver',
            'amount',
            'fees',
            'service_type',
            'service_name',
            'balance_before',
            'balance_after',
            'transaction_date',
            # 'user_wallet',  # Uncomment if you want to include user_wallet details
        ]

    def get_sender(self, obj):
        return obj.sender.phone_number  # Return the sender's phone number


class SendMoneySerializer(serializers.Serializer):
    reciever_number = serializers.CharField(max_length=15)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_reciever_number(self, value):
        user = self.context['request'].user
        if value == user.phone_number:
            raise serializers.ValidationError("You can't make a transaction to yourself!")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        try:
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Wallet does not exist for the user.")

        if data['amount'] > wallet.balance:
            raise serializers.ValidationError("Insufficient funds!")
        return data


class WithdrawalSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.CharField(max_length=50)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        try:
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Wallet does not exist for the user.")

        if data['amount'] > wallet.balance:
            raise serializers.ValidationError("Insufficient funds!")
        return data
