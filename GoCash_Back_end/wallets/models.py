from django.db import models
from users.models import User
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal


class Wallet(models.Model):
    wallet_id = models.AutoField(primary_key=True)
    wallet_pass = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

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

    def reset_password(self, new_password):
        """Reset wallet password for the user"""
        self.wallet_pass = new_password
        self.save()
        return new_password

    def initial_deletion(self, deleted_wallet_model):
        """Add the wallet object to deleted wallets table and set the initial and final deletion date
        Three-day deadline"""
        self.deleted = True
        self.is_active = False
        self.save()

        del_wallet = deleted_wallet_model.objects.create(
            user=self.user,
            balance=self.balance,
        )
        del_wallet.final_deletion_date = del_wallet.initial_deletion_date + timedelta(days=3)
        del_wallet.save()

    def final_deletion(self, deleted_wallet_model):
        """Delete the Wallet permanently from Wallet table"""
        if timezone.now() >= deleted_wallet_model.final_deletion_date:
            deleted_wallet_model.deletion_confirmation = True
            deleted_wallet_model.save()
            self.delete()
        else:
            rem_days = deleted_wallet_model.final_deletion_date - timezone.now()
            rem_days = rem_days.total_seconds()
            hours = int(rem_days // 3600)
            minutes = int((rem_days % 3600) // 60)
            return f'{hours} h and {minutes} m till permanent deletion!'

    def wallet_restore(self, deleted_wallet_model):
        # Ensure the final_deletion_date is properly fetched from the database
        final_deletion_date = deleted_wallet_model.final_deletion_date
        print(final_deletion_date)
        if final_deletion_date and timezone.now() < final_deletion_date:
            self.is_active = True
            self.deleted = False
            self.save()
            deleted_wallet_model.delete()
        else:
            return 'Cannot restore, deletion period has passed.'

    def wallet_activation(self, state):
        if isinstance(state, bool):
            self.is_active = state
            self.save()
        else:
            return 'Invalid entry'


class DeletedWallets(models.Model):
    wallet_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    initial_deletion_date = models.DateTimeField(auto_now_add=True)
    final_deletion_date = models.DateTimeField(blank=True, null=True)
    deletion_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Deleted Wallet"
