import psycopg2
import random
from datetime import datetime, timedelta
from faker import Faker
import re

fake = Faker()

# Database connection settings
connection = psycopg2.connect(
    dbname="demoDB",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

SERVICE_TYPES = ["Deposit", "Withdrawal", "Transfer", "Payment"]
SERVICE_NAMES = ["Wallet Charge", "Bill Payment", "Merchant Payment"]



def generate_phone_number():
    phone_number = re.sub(r'\D', '', fake.phone_number())  # Remove non-digit characters
    return phone_number[:11]  # Limit to 11 digits



def populate_tables(user_count, transaction_count):
    user_ids = []
    for _ in range(user_count):
        phone_number = generate_phone_number()
        username = fake.user_name()
        registration_date = fake.date_time_between(start_date="-3y", end_date="now")
        subscription_plan_id = random.choice([1, 2, 3])  # Assuming three subscription plans
        green_user_status_id = random.choice([1, 2, 3, None])  # Some users may not have green status

        # Insert a user
        cursor.execute(
            """
            INSERT INTO Users (phone_number, username, registration_date, subscription_plan_id, green_user_status_id, is_active, is_staff)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING user_id
            """,
            (phone_number, username, registration_date, subscription_plan_id, green_user_status_id, True, False)
        )
        user_id = cursor.fetchone()[0]
        user_ids.append(user_id)

        # Create a wallet for the user
        wallet_pass = ''.join(random.choices("0123456789", k=6))
        balance = round(random.uniform(0, 5000), 2)
        cursor.execute(
            """
            INSERT INTO Wallet (wallet_pass, user_id, balance, is_active, deleted)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING wallet_id
            """,
            (wallet_pass, user_id, balance, True, False)
        )
        wallet_id = cursor.fetchone()[0]
    print('Data inserted into Tables User & Wallet successfully!')

    # Generate transactions
    for _ in range(transaction_count):
        sender_id = random.choice(user_ids)
        receiver_phone = generate_phone_number()
        amount = round(random.uniform(1, 500), 2)
        fees = round(amount * 0.02, 2)
        balance_before = random.uniform(0, 1000)
        balance_after = balance_before - amount
        transaction_date = fake.date_time_between(start_date="-3y", end_date="now")
        service_type = random.choice(SERVICE_TYPES)
        service_name = random.choice(SERVICE_NAMES)

        cursor.execute(
            """
            INSERT INTO Transaction (sender_id, receiver, user_wallet_id, amount, fees, service_type, service_name, balance_before, balance_after, transaction_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (sender_id, receiver_phone, wallet_id, amount, fees, service_type, service_name, balance_before,
             balance_after, transaction_date)
        )
    print('Data inserted into Transaction table successfully!')

    connection.commit()
    print("Dynamic data population complete.")


def populate_dynamic_tables():
    user_ids = []
    year_data = {
        2021: {'total_users': 5000, 'green_users': 500},
        2022: {'total_users': 20000, 'green_users': 2800},
        2023: {'total_users': 200000, 'green_users': 80000},
        2024: {'total_users': 380000, 'green_users': 125000},
    }
    user_counter = 1

    for year, data in year_data.items():
        total_users = data['total_users']
        green_users = data['green_users']

        for i in range(total_users):
            phone_number = f"USER-{user_counter}"  # Unique identifier for each user
            user_counter += 1  # Increment the counter for uniqueness
            username = fake.user_name()

            # Generate a registration date within the current year
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            # registration_date = fake.date_time_between(
            #     start_date=f"{year}-01-01",
            #     end_date=f"{year}-12-31"
            # )
            registration_date = fake.date_time_between(
                start_date=start_date,
                end_date=end_date
            )

            subscription_plan_id = random.choice([4, 5, 6])  # Assuming three subscription plans

            # Assign green_user_status_id based on the ratio of green users
            if i < green_users:
                green_plan_status_id = random.choice([1, 2, 3])  # Green user
            else:
                green_plan_status_id = None  # Not a green user

            # Insert a user
            cursor.execute(
                """
                INSERT INTO Users (phone_number, username, registration_date, subscription_plan_id, green_plan_status_id, is_active, is_staff)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING user_id
                """,
                (phone_number, username, registration_date, subscription_plan_id, green_plan_status_id, True, False)
            )
            user_ids.append(cursor.fetchone()[0])
    connection.commit()
    print("Data Inserted Successfully")


def populate_transactions(year, year_data):
    service_counts = year_data[year]  # Get transaction data for the given year

    for service_type_, transaction_count in service_counts.items():
        for _ in range(transaction_count):
            sender_id = 691105
            receiver_phone = generate_phone_number()
            wallet_id = 1
            amount = round(random.uniform(500, 10000), 2)
            fees = round(amount * 0.02, 2)
            balance_before = round(random.uniform(10000, 30000), 2)
            balance_after = round(balance_before - amount, 2)

            if service_type_ == "deposit":
                balance_after = round(balance_before + amount, 2)  # Simulate deposit

            service_type = service_type_.capitalize()
            service_name = random.choice(SERVICE_NAMES)

            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            transaction_date = fake.date_time_between(
                start_date=start_date,
                end_date=end_date
            )

            cursor.execute(
                """
                INSERT INTO Transaction (sender_id, receiver, user_wallet_id, amount, fees, service_type, service_name, balance_before, balance_after, transaction_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (sender_id, receiver_phone, wallet_id, amount, fees, service_type, service_name, balance_before,
                 balance_after, transaction_date)
            )

    connection.commit()
    print(f"Done Inserting transactions fot year: {year}")





year_data = {
    2021: {"deposit": 3000, "withdrawal": 2500, "payment": 300, "transfer": 4600},
    2022: {"deposit": 15000, "withdrawal": 13400, "payment": 4200, "transfer": 38000},
    2023: {"deposit": 160000, "withdrawal": 102000, "payment": 30200, "transfer": 315000},
    2024: {"deposit": 310000, "withdrawal": 260000, "payment": 102000, "transfer": 568000},
}


try:
    # populate_dynamic_tables(user_count=30000, transaction_count=100000)
    # populate_dynamic_tables()
    for year in year_data:
        populate_transactions(year, year_data)
finally:
    cursor.close()
    connection.close()
    print("Database connection closed.")
