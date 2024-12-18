from rest_framework import serializers
from transactions.models import Transaction
from wallets.models import Wallet
from decimal import Decimal


class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    service_type = serializers.CharField(max_length=50)
    service_name = serializers.CharField(max_length=50)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        wallet = Wallet.objects.get(user=user)
        if data['amount'] > wallet.balance:
            raise serializers.ValidationError("Insufficient funds!")
        return data
