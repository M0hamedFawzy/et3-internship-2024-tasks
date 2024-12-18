from Classes import Account, Wallet, Transaction, Payment, GreenUser

def main_menu():
    print("Welcome to the Mobile Payment Application")
    print("1. Register")
    print("2. Sign In")
    print("3. Exit")
    return input("Please choose an option: ")

def post_login_menu():
    print("\nWelcome to the application!")
    print("1. Wallet")
    print("2. Transactions")
    print("3. Payments")
    print("4. Green Subscription")
    print("5. Sign Out")
    return input("Please choose an option: ")

def wallet_menu(wallet):
    print("\nWallet Menu")
    print("1. Check Balance")
    print("2. Back")
    return input("Please choose an option: ")

def transactions_menu(transaction):
    print("\nTransactions Menu")
    print("1. Send Money")
    print("2. Receive Money")
    print("3. Transaction History")
    print("4. Back")
    return input("Please choose an option: ")

def payments_menu(payment):
    print("\nPayments Menu")
    print("1. Make a Bill Payment")
    print("2. Charge Balance using Service Code")
    print("3. Back")
    return input("Please choose an option: ")

def green_subscription_menu(green_user):
    print("\nGreen Subscription Menu")
    print("1. Subscribe")
    print("2. Renew Subscription")
    print("3. Cancel Subscription")
    print("4. Back")
    return input("Please choose an option: ")

def run_application():
    account = Account()
    user_logged_in = False
    wallet = None
    transaction = None
    payment = None
    green_user = None

    while True:
        if not user_logged_in:
            choice = main_menu()

            if choice == '1':
                # Register
                phone_no = input("Enter your phone number: ")
                name = input("Enter your name: ")
                account.sign_up(name, phone_no)
                print("Now you can sign in.")
            elif choice == '2':
                # Sign In
                phone_no = input("Enter your phone number: ")
                if account.sign_in(str(phone_no)):
                    user_logged_in = True
                    wallet = Wallet(account)
                    transaction = Transaction(account)
                    payment = Payment(account)
                    green_user = GreenUser(account)
                else:
                    print("Sign In Failed. Please register first.")
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

        else:
            choice = post_login_menu()

            if choice == '1':  # Wallet operations
                while True:
                    wallet_choice = wallet_menu(wallet)
                    if wallet_choice == '1':
                        print(f"Your current balance is: {wallet.get_balance()}")
                    elif wallet_choice == '2':
                        break
                    else:
                        print("Invalid option. Please try again.")

            elif choice == '2':  # Transactions
                while True:
                    trans_choice = transactions_menu(transaction)
                    if trans_choice == '1':
                        receiver = input("Enter receiver's phone number: ")
                        amount = float(input("Enter the amount to send: "))
                        transaction.send(receiver, amount)
                    elif trans_choice == '2':
                        transaction.recieve()
                    elif trans_choice == '3':
                        transaction.display_transactions_hstory()
                    elif trans_choice == '4':
                        break
                    else:
                        print("Invalid option. Please try again.")

            elif choice == '3':  # Payments
                while True:
                    payment_choice = payments_menu(payment)
                    if payment_choice == '1':
                        payment.bills_payment()
                    elif payment_choice == '2':
                        service_code = input("Enter the service code: ")
                        amount = float(input("Enter the amount to charge: "))
                        payment.charge_balance(amount, service_code)
                    elif payment_choice == '3':
                        break
                    else:
                        print("Invalid option. Please try again.")

            elif choice == '4':  # Green Subscription
                while True:
                    green_choice = green_subscription_menu(green_user)
                    if green_choice == '1':
                        green_user.green_subscribtion()
                    elif green_choice == '2':
                        green_user.subscription_renewal()
                    elif green_choice == '3':
                        green_user.cansel_subscription()
                    elif green_choice == '4':
                        break
                    else:
                        print("Invalid option. Please try again.")

            elif choice == '5':
                print("You have signed out.")
                user_logged_in = False

            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    run_application()
