from datetime import datetime
import datetime
import calendar
import os
import csv
import time
from datetime import date
import Classes
# account = Classes.Account()

# choice = input('For Register Please press 1 \nFor Sign up new Account press 2\nFor User Info press 3\nyour choice : ')
# if choice == '1':
#     phone_number = input('Please enter your phone number ')
#     Classes.Account.register(account, phone_no= phone_number)
# elif choice == '2':
#     phone_number = input('To sign up new account Please enter your phone number : ')
#     name = input('now enter your user name : ')
#     Classes.Account.sign_up(account, name=name, phone_no=phone_number)
# elif choice == '3':
#     phone_number = input('Please enter your phone number ')
#     Classes.Account.register(account, phone_no=phone_number)
#     trans = Classes.Transaction(account)
#     Classes.Transaction.print_user_info(trans)

# def generate_custom_code(phoneNo, name):
#     first_part = phoneNo[:7]
#     sum_digits = sum(int(ch) for ch in first_part)
#     sum_ascii = sum(ord(ch) for ch in name)
#     totalsum = sum_ascii + sum_digits
#     totalsum = totalsum % 1000
#     totalsum = f"{totalsum:04}"
#     last_part = phoneNo[-4:]
#     result = f"{last_part}{totalsum}"
#     return result


# def sum_to_4_digits(*numbers):
#     total_sum = sum(numbers)
#
#     # Ensure the sum stays within 4 digits by using modulo 10000
#     result = total_sum % 10000
#
#     # Format the result to always be 4 digits, with leading zeros if necessary
#     return f"{result:04}"





# phoneNo = "01126008231"
# name = "Mohamed Fawzy"
# result = generate_custom_code(phoneNo, name)
# print(result)


def create_transactions_file():
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


# create_transactions_file()
# userId = 12345678
# action = 'send'
# amount = 100
# currentdate = date.today()
# time_stamp = time.time()
# sender = "01126008231"
# receiver = "01143874955"
# status = 'pending'
# transaction_data = [userId, action, amount, currentdate, time_stamp, sender, receiver, status]
# with open('transaction_send.csv', mode='a', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(transaction_data)
# phoneNo = '01143874955'
# id = 87654321
# total_sum = 0
# rows = []
# copied_rows = []
# cdate = date.today()
# time_stamp = time.time()
# with open('transaction_send.csv', mode='r', newline='') as sendFile:
#     reader = csv.reader(sendFile)
#     header = next(reader)
#     for row in reader:
#         if row[6] == phoneNo and row[7] == 'pending':
#             copied_row = row[:-1]
#             copied_row[0] = id
#             copied_row[3] = cdate
#             copied_row[4] = time_stamp
#             copied_rows.append(copied_row)
#             print(f'You have recieved a total of {copied_row[2]}$ from Phone Number {copied_row[4]}\nDate : {copied_row[3]}\n')
#             total_sum += int(copied_row[2])
#             row[7] = 'done'
#         rows.append(row)
#     print(f'Your total received amount is {total_sum}$')
# # print(copied_rows)
# with open('transaction_send.csv', mode='w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(header)
#     writer.writerows(rows)
#
#
# with open('transaction_recieve.csv', mode='a', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerows(copied_rows)
#     print('Transactions added to your account Successfully!')

# def debug_csv():
#     input_csv = 'transaction_send.csv'
#
#     with open(input_csv, mode='r', newline='') as infile:
#         reader = csv.reader(infile)
#         header = next(reader)  # Skip the header
#         print(f"CSV Header: {header}")
#
#         for row in reader:
#             print(f"CSV Row: {row}")  # Print each row to check the structure
#             print(f"Receiver: {row[5]}, Status: {row[6]}")  # Debug specific columns


# Example usage
# debug_csv()


def display_transactions_hstory():
    send_transactions = []
    recived_transactions = []
    user_id = '87654321'
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

    sorted_transactions = []
    for transaction in all_transactions:
        try:
            # Parse the date; if it fails, skip this transaction
            transaction_date = datetime.strptime(transaction[4], "%m/%d/%Y")
            sorted_transactions.append((transaction_date, transaction))
        except (ValueError, IndexError) as e:
            print(f"Skipping transaction due to date format issue: {transaction}")

    # Sort the valid transactions by date, newest first
    sorted_transactions.sort(key=lambda x: x[0], reverse=True)

    # Extract and display sorted transactions (discard the datetime objects)
    for date, transaction in sorted_transactions:
        print(transaction)


# display_transactions_hstory()


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

start_date = date.today()

# renewal_date = add_months(start_date, 1)
# print(renewal_date)

current_date = date.today()
today_str = '2024-09-07'

# print(str(current_date) == today_str)

if 4==4 and not 5 == 6:
    print('not equal')