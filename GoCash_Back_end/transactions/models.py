from django.db import models
from django.shortcuts import get_object_or_404
from users.models import User
from wallets.models import Wallet
from SubscriptionPlan.models import SubscriptionPlan, PlanSubscribedUsers
from GreenPlan.models import GreenPlan, GreenSubscribedUsers
from decimal import Decimal


class Transaction(models.Model):
    SERVICE_TYPE = [
        ('Deposit', 'deposit'),
        ('Withdrawal', 'withdrawal'),
        ('Transaction', 'transaction'),
        ('Bill Payment', 'bill payment'),
        ('Mobile Bills', 'mobile bills'),
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
        return f"{self.transaction_id} - {self.sender.username}"

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

    @classmethod
    def process_pay(cls, user, wallet, amount, service_type, service_name, tax=0.02):
        """ Handel payment logic"""
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
            service_type=service_type,
            service_name=service_name,
            balance_before=old_balance,
            balance_after=new_balance,
        )

        return f"After fees and Green discount(if any). The Payment amount is {(amount + fees):.2f} EGP"

    @classmethod
    def process_subscribe(cls, user, wallet, subscription_plan, sub_start_date):
        user.subscription_plan_id = subscription_plan.id
        sub_price = subscription_plan.price
        old_balance = Decimal(wallet.balance)
        new_balance = old_balance - sub_price
        wallet.balance = new_balance
        wallet.save()
        user.save()

        PlanSubscribedUsers.create_subscription_history(
            user_p_n=user.phone_number,
            plan=subscription_plan,
            sub_start_date=sub_start_date
        )

        cls.create_transaction(
            sender=user,
            receiver=user.phone_number,
            user_wallet=wallet,
            amount=sub_price,
            fees=0,
            service_type="Account Subscription",
            service_name=f'{subscription_plan.name} Plan',
            balance_before=old_balance,
            balance_after=new_balance,
        )

        return f"User Subscribed Successfully to the {subscription_plan.name} Plan. Monthly fees {(subscription_plan.price):.2f} EGP/Month"

    @classmethod
    def process_green_subscribe(cls, user, wallet, g_plan, sub_start_date):
        user.green_user_status_id = g_plan.id
        sub_price = g_plan.price
        old_balance = Decimal(wallet.balance)
        new_balance = old_balance - sub_price
        wallet.balance = new_balance
        wallet.save()
        user.save()

        GreenSubscribedUsers.create_green_subscription_history(
            user_p_n=user.phone_number,
            g_plan=g_plan,
            sub_start_date=sub_start_date
        )

        cls.create_transaction(
            sender=user,
            receiver=user.phone_number,
            user_wallet=wallet,
            amount=sub_price,
            fees=0,
            service_type="Green Subscription",
            service_name=f'{g_plan.green_type} Plan',
            balance_before=old_balance,
            balance_after=new_balance,
        )

        return f"User Subscribed Successfully to the {g_plan.green_type} Green Plan. Monthly fees {(g_plan.price):.2f} EGP/Month. Thanks for making the environment everyday better."


