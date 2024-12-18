from datetime import datetime
import os
import csv
from datetime import date
import time
import calendar

class User:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def diaplay_user_info(self):
        print(f'User Name : {self.name}\nPhone No. : {self.phone_number}')

    def get_user_info(self):
        return self.phone_number, self.name



class Account:
    userObj = User
    def __init__(self):
        self.userObj = None

    def __createUsersFile(self):
        with open('users_file.txt', 'w'):
            pass

    def __checkUsersFileExist(self):
        return os.path.isfile('users_file.txt')

    def __checkUserAccountExist(self, phone_no):
        with open('users_file.txt', 'r') as file:
            for line in file:
                stored_p_no = line.strip().split(maxsplit=1)
                if phone_no == stored_p_no[0]:
                    return True
            return False


    def __writeUserFile(self, name, phone_no):
        with open('users_file.txt', 'a') as file:
            file.write(f'{phone_no} {name}\n')

    def __getUserInfo(self, phone_no):
        with open('users_file.txt', 'r') as file:
            for line in file:
                stored_data = line.strip().split(maxsplit=1)
                if stored_data[0] == phone_no:
                    return stored_data[0], stored_data[1]

    def sign_in(self, phone_no):
        if self.__checkUsersFileExist():
            if self.__checkUserAccountExist(phone_no):
                Pnumber, name = self.__getUserInfo(phone_no)
                self.userObj = User(name, Pnumber)
                print("User signed in Successfully!")
                return True
            else:
                print('there is no account exists with this phone number')
        else:
            self.__createUsersFile()
            print('there is no account exists with this phone number')
        return False

    def sign_up(self,name, phone_no):
        if not self.__checkUsersFileExist():
            self.__createUsersFile()
        if not self.__checkUserAccountExist(phone_no):
            self.__writeUserFile(name=name, phone_no=phone_no)
            self.userObj = User(name, phone_no)
            print('you have signed up successfully!')
        else:
            print('your Phone No. has an account. Please Sign In')







class Wallet:

    def __init__(self, account):
        self.accountObj = account
        if self.accountObj.userObj:
            self.phoneNo, _ = self.accountObj.userObj.get_user_info()
        else:
            self.phoneNo = None

    def __create_user_wallet(self):
        if not os.path.isfile('wallet_file.txt'):
            with open('wallet_file.txt', 'w'):
                pass

        phonesExist = False
        with open('wallet_file.txt', 'r') as file:
            for line in file:
                data = line.strip().split()
                pNo = data[0]
                if pNo == self.phoneNo:
                    phonesExist = True
                    break

            if not phonesExist:
                with open('wallet_file.txt', 'a') as file:
                    file.write(f'{self.phoneNo} {0}\n')

    def __write_walletFile(self, newBalance):
        self.__create_user_wallet()
        file_data = []

        with open('wallet_file.txt', 'r') as file:
            for line in file:
                data = line.strip().split()
                pNo = data[0]

                if pNo == self.phoneNo:
                    new_row = f'{self.phoneNo} {newBalance}\n'
                    file_data.append(new_row)
                else:
                    file_data.append(line)

        with open('wallet_file.txt', 'w') as file:
            file.writelines(file_data)

    def get_balance(self):
        self.__create_user_wallet()
        with open('wallet_file.txt', 'r') as file:
            for line in file:
                data = line.strip().split()
                pNo = data[0]
                if pNo == self.phoneNo:
                    return float(data[1])

    def increase_balance(self, amount):
        self.__create_user_wallet()
        current_balance = self.get_balance()
        new_balance = float(current_balance) + amount
        self.__write_walletFile(newBalance=new_balance)

    def decrease_balance(self, amount):
        self.__create_user_wallet()
        current_balance = self.get_balance()
        new_balance = float(current_balance) - amount
        self.__write_walletFile(newBalance=new_balance)







class Transaction:
    def __init__(self, account):
        self.accountObj = account
        if self.accountObj.userObj:
            self.phoneNo, self.name = self.accountObj.userObj.get_user_info()
        else:
            pass

        self.walletObj = Wallet(self.accountObj)

    def __id_generator(self):
        first_part = self.phoneNo[:7]
        sum_digits = sum(int(ch) for ch in first_part)
        sum_ascii = sum(ord(ch) for ch in self.name)
        totalsum = sum_ascii + sum_digits
        totalsum = totalsum % 1000
        totalsum = f"{totalsum:04}"
        last_part = self.phoneNo[-4:]
        id = f"{last_part}{totalsum}"
        return id

    def __create_transactions_file(self):
        if not os.path.isfile('transaction_send.csv'):
            with open('transaction_send.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'action', 'amount', 'date', 'timestamp', 'sender', 'receiver', 'status'])
        else:
            pass
        if not os.path.isfile('transaction_recieve.csv'):
            with open('transaction_recieve.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'action', 'amount', 'date', 'timestamp', 'sender', 'receiver'])
        else:
            pass

    def send(self, receiver, amount):
        self.__create_transactions_file()
        userId = self.__id_generator()
        sender = self.phoneNo
        status = 'pending'
        currentdate = date.today()
        time_stamp = time.time()
        action = 'send'
        transaction_data = [userId, action, amount, currentdate, time_stamp, sender, receiver, status]
        currentBalance = self.walletObj.get_balance()
        if amount > float(currentBalance):
            print('insufficient funds')
        else:
            self.walletObj.decrease_balance(amount=amount)
            with open('transaction_send.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(transaction_data)

    def recieve(self):
        self.__create_transactions_file()
        id = self.__id_generator()
        reciveDate = date.today()
        time_stamp = time.time()
        recivedAmount = 0
        rows = []
        copied_rows = []
        with open('transaction_send.csv', mode='r', newline='') as sendFile:
            reader = csv.reader(sendFile)
            header = next(reader)
            for row in reader:
                if row[6] == self.phoneNo and row[7] == 'pending':
                    copied_row = row[:-1]
                    copied_row[0] = id
                    copied_row[3] = reciveDate
                    copied_row[4] = time_stamp
                    copied_row[1] = 'received'
                    copied_rows.append(copied_row)
                    print(f'You have recieved a total of {copied_row[2]}$ from Phone Number {copied_row[5]}\nDate : {copied_row[3]}\n')
                    recivedAmount += float(copied_row[2])
                    row[7] = 'done'
                rows.append(row)

        with open('transaction_send.csv', mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            writer.writerows(rows)

        if recivedAmount == 0:
            print('Thers is no received transactions to show!')
        else:
            with open('transaction_recieve.csv', mode='a', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(copied_rows)

            self.walletObj.increase_balance(recivedAmount)
            print(f'Your total received amount is {recivedAmount}$')
            print(f'Transactions added to your Wallet Successfully!\nYour New Balance is : {self.walletObj.get_balance()}\n')

    def display_transactions_hstory(self):
        send_transactions = []
        recived_transactions = []
        user_id = self.__id_generator()
        with open('transaction_send.csv', mode='r', newline='') as sendFile:
            reader = csv.reader(sendFile)
            for row in reader:
                if row[0] == user_id:
                    send_transactions.append(row)

        with open('transaction_recieve.csv', mode='r', newline='') as sendFile:
            reader = csv.reader(sendFile)
            for row in reader:
                if row[0] == user_id:
                    recived_transactions.append(row)

        all_transactions = send_transactions + recived_transactions
        all_transactions.sort(key=lambda x: float(x[4]), reverse=True)

        for transaction in all_transactions:
            print(transaction)





class Payment:

    payments = {
        "Mobile Payments": [
            {"amount": 350, "description": "We Internet"},
            {"amount": 80, "description": "Recharge"},
            {"amount": 300, "description": "Mobile Bills"}
        ],
        "Bill Payments": [
            {"amount": 120, "description": "Electricity"},
            {"amount": 240, "description": "Gas"},
            {"amount": 150, "description": "Water"},
            {"amount": 199, "description": "TV Subscription"}
        ]
    }

    def __init__(self, account):
        self.acountObj = account
        self.walletObj = Wallet(self.acountObj)

    def charge_balance(self, amount, service_code):
        with open('payment_service.txt', 'r') as file:
            for line in file:
                data_ = line.strip().split(maxsplit=1)
                code_ = data_[0]
                payment_method = data_[1]
                if service_code == code_:
                    print(f'you are using {payment_method} payment service. Your charged amount is {amount}.')
                    self.walletObj.increase_balance(amount=amount)
                    print('your balance has been Updated!')
                    print(f'Your new Balance is {self.walletObj.get_balance()}')


    def bills_payment(self):
        print("Please choose a payment type:")
        for i, category in enumerate(self.payments.keys(), 1):
            print(f"{i}. {category}")

        payment_choice = int(input("Enter the number corresponding to your choice: ")) - 1
        payment_type = list(self.payments.keys())[payment_choice]
        print(f"\nYou chose {payment_type}. Now, choose a service:")

        for i, service in enumerate(self.payments[payment_type], 1):
            print(f"{i}. {service['description']}")

        service_choice = int(input("Enter the number corresponding to your chosen service: ")) - 1
        chosen_service = self.payments[payment_type][service_choice]

        print(f"\nYou chose {chosen_service['description']}. The required price is {chosen_service['amount']}.")
        choice = input('Do you want to proceed with payment? y/n')

        if choice == 'y':
            self.walletObj.decrease_balance(chosen_service['amount'])
            print('payment done successfully!')
        else:
            print('Payment has been cancelled')





class GreenUser:

    def __init__(self, account):
        self.acountObj = account

        if self.acountObj.userObj:
            self.phoneNo, _ = self.acountObj.userObj.get_user_info()
        else:
            pass
        self.walletObj = Wallet(self.acountObj)

    def __create_green_users_file(self):
        if os.path.isfile('green_users.txt'):
            pass
        else:
            with open('green_users.txt', 'w'):
                pass

    def __add_months(self, sourcedate, months):
        if isinstance(sourcedate, int):
            raise TypeError("sourcedate must be a datetime object, not an integer")

        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])

        return datetime(year, month, day)

    def green_subscribtion(self):
        self.__create_green_users_file()
        acount_exist = False
        with open('green_users.txt', 'r') as file:
            for line in file:
                pNo, _, _, _, _ = line.strip().split()
                if pNo == self.phoneNo:
                    acount_exist = True
                    break

        if acount_exist:
            print('you have already Subscribed')
        else:
            if float(self.walletObj.get_balance()) < 200:
                print('you done\'t have enough balance to subscribe')
            else:
                start_date = date.today()
                print(start_date)
                renewal_date = self.__add_months(start_date, 1)
                plan = int(input('Choose a Subscribtion plan.\n1. 2.5% / month\n2. 5% / month\n3. 7% / month\n'))
                if plan == 1:
                    with open('green_users.txt', 'a') as file:
                        file.write(f'{self.phoneNo} {2.5} {start_date} {renewal_date}\n')
                        subscribtion_fees = float(self.walletObj.get_balance()) * 2.5 / 100
                        self.walletObj.decrease_balance(self.walletObj.get_balance() - subscribtion_fees)
                        print('you have subscribed successfully!')

                elif plan == 2:
                    with open('green_users.txt', 'a') as file:
                        file.write(f'{self.phoneNo} {5} {start_date} {renewal_date}\n')
                        subscribtion_fees = float(self.walletObj.get_balance()) * 5 / 100
                        self.walletObj.decrease_balance(self.walletObj.get_balance() - subscribtion_fees)
                        print('you have subscribed successfully!')
                elif plan == 3:
                    with open('green_users.txt', 'a') as file:
                        file.write(f'{self.phoneNo} {7} {start_date} {renewal_date}\n')
                        subscribtion_fees = float(self.walletObj.get_balance()) * 7 / 100
                        self.walletObj.decrease_balance(self.walletObj.get_balance() - subscribtion_fees)
                        print('you have subscribed successfully!')
                else:
                    print('Invalid entry. Try Again!')

    def subscription_renewal(self):
        modified_lines = []
        current_date = date.today()
        with open('green_users.txt', 'r') as file:
            for line in file:
                pNo, plan, start_date, renewal_date, ts = line.strip().split()
                if pNo == self.phoneNo and str(current_date) == renewal_date:
                    start_date = renewal_date
                    renewal_date = self.__add_months(start_date, 1)
                    subFees = float((self.walletObj.get_balance() * float(plan)) / 100)
                    self.walletObj.decrease_balance(self.walletObj.get_balance() - subFees)
                    print('your subscription has been renewed.')
                elif pNo == self.phoneNo and not str(current_date) == renewal_date:
                    print('your subscription has not yet expired.')
                else:
                    pass

                modified_line = f"{pNo} {plan} {start_date} {renewal_date} {ts}\n"
                modified_lines.append(modified_line)

        with open('green_users.txt', 'w') as file:
            file.writelines(modified_lines)

    def cansel_subscription(self):
        modified_subscribers = []
        with open('green_users.txt', 'r') as file:
            for line in file:
                pNo, plan, start_date, renewal_date, ts = line.strip().split()
                if pNo == self.phoneNo:
                    print('Subscription has been canceled')
                    continue
                modified_subscribers = f"{pNo} {plan} {start_date} {renewal_date} {ts}\n"

        with open('green_users.txt', 'w') as file:
            file.writelines(modified_subscribers)