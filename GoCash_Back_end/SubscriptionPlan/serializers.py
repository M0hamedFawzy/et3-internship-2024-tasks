from rest_framework import serializers
from transactions.models import Transaction
from wallets.models import Wallet
from decimal import Decimal


class SubscriptionPlanSerializer(serializers.Serializer):
    plan_name = serializers.CharField(max_length=10)
    plan_price = serializers.DecimalField(max_digits=6, decimal_places=2)

    def validate_name(self, value):
        if value not in ['Standard', 'Plus', 'Premium']:
            raise serializers.ValidationError("Invalid Plan.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        wallet = Wallet.objects.get(user=user)
        if data['plan_price'] > wallet.balance:
            raise serializers.ValidationError("Insufficient funds!")
        return data
