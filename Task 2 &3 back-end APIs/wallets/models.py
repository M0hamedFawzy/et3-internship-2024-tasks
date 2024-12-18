from django.db import models
from users.models import User
from decimal import Decimal


class Wallet(models.Model):
    wallet_id = models.AutoField(primary_key=True)
    wallet_pass = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - Wallet"

    def check_password(self, entered_pass):
        """Check if the entered password matches the wallet's password."""
        return self.wallet_pass == entered_pass

    @classmethod
    def create_wallet(cls, user, password):
        """Create a new wallet for a user."""
        wallet = cls.objects.create(wallet_pass=password, user=user, balance=0)
        return wallet

    def charge_wallet(self, amount, payment_method, transaction_model):
        """Charge the wallet with a specified amount and create a transaction."""
        if amount <= 0:
            raise ValueError('Amount must be greater than zero')

        old_balance = self.balance
        new_balance = old_balance + amount

        # Create a new transaction
        transaction_model.objects.create(
            sender=self.user,
            receiver=self.user.phone_number,
            user_wallet=self,
            amount=amount,
            fees=0,
            service_type='Deposit',
            service_name=f"Wallet Charge ({payment_method})",
            balance_before=old_balance,
            balance_after=new_balance,
        )

        # Update the wallet balance
        self.balance = new_balance
        self.save()
        return self.balance
