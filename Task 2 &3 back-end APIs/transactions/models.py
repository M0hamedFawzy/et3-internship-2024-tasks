from django.db import models
from django.shortcuts import get_object_or_404
from users.models import User
from wallets.models import Wallet
from decimal import Decimal


class Transaction(models.Model):
    SERVICE_TYPE = [
        ('Deposit', 'deposit'),
        ('Withdrawal', 'withdrawal'),
        ('Transaction', 'transaction'),
        ('Bill Payment', 'bill payment'),
        ('Merchant Payment', 'merchant payment'),
        ('Account Subscription', 'account subscription'),
        ('Green Subscription', 'green subscription'),
    ]

    transaction_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    receiver = models.CharField(max_length=15)
    user_wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING, related_name='user_wallet')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE, null=True)
    service_name = models.CharField(max_length=50, null=True, blank=True)
    balance_before = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.sender}"

    @classmethod
    def create_transaction(cls, sender, receiver, user_wallet, amount, service_type, service_name, balance_before,
                           balance_after, fees=0):
        """Create a new transaction and save it."""
        cls.objects.create(
            sender=sender,
            receiver=receiver,
            user_wallet=user_wallet,
            amount=amount,
            service_type=service_type,
            service_name=service_name,
            balance_before=balance_before,
            balance_after=balance_after,
            fees=fees,
        )

    @classmethod
    def process_send_money(cls, user, rec_user, rec_number, wallet, amount, tax=0.10):
        """Handle the logic for sending money."""
        old_balance = Decimal(wallet.balance)
        if rec_user is None:
            """Make transaction for sender only."""
            fees = amount * Decimal(tax)
            new_balance = old_balance - (amount + fees)
            wallet.balance = new_balance
            wallet.save()
            cls.create_transaction(
                sender=user,
                receiver=rec_number,
                user_wallet=wallet,
                amount=amount,
                fees=fees,
                service_type='Transaction',
                service_name="Non Subscribed User",
                balance_before=old_balance,
                balance_after=new_balance,
            )
            return f"After fees, the sent amount is {(amount + fees):.2f} to {rec_number}"
        else:
            """Make transaction for sender."""
            new_balance = old_balance - amount
            wallet.balance = new_balance
            wallet.save()
            cls.create_transaction(
                sender=user,
                receiver=rec_user.phone_number,
                user_wallet=wallet,
                amount=amount,
                fees=0,
                service_type='Transaction',
                service_name="GoCash User",
                balance_before=old_balance,
                balance_after=new_balance,
            )
            """Make transaction for receiver."""
            rec_wallet = get_object_or_404(Wallet, user=rec_user)
            rec_old_balance = Decimal(rec_wallet.balance)
            rec_new_balance = rec_old_balance + amount
            rec_wallet.balance = rec_new_balance
            rec_wallet.save()
            cls.create_transaction(
                sender=user,
                receiver=rec_user.phone_number,
                user_wallet=rec_wallet,
                amount=amount,
                fees=0,
                service_type='Transaction',
                service_name="GoCash User",
                balance_before=rec_old_balance,
                balance_after=rec_new_balance,
            )
            return f"Amount sent successfully to {rec_user.username}."

    @classmethod
    def process_withdrawal(cls, user, wallet, amount, method, tax=0.04):
        """Handle the logic for withdrawing money."""
        old_balance = Decimal(wallet.balance)
        fees = amount * Decimal(tax)
        new_balance = old_balance - (amount + fees)
        wallet.balance = new_balance
        wallet.save()
        cls.create_transaction(
            sender=user,
            receiver=user.phone_number,
            user_wallet=wallet,
            amount=amount,
            fees=fees,
            service_type='Withdrawal',
            service_name=method,
            balance_before=old_balance,
            balance_after=new_balance,
        )

        return f"After fees, the sent amount is {(amount + fees):.2f}"


