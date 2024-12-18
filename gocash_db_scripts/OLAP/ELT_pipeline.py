import psycopg2
from psycopg2.extras import execute_values

# Database configuration
DB_CONFIG = {
    "dbname": "DWBI",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}


# ELT Pipeline Functions
def connect_to_db(config):
    """Establishes connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise


def execute_query(cursor, query):
    """Executes a single query."""
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error executing query: {e}")
        raise


def populate_dim_date(cursor):
    """Populates the DimDate table. from 2022 t0 2024"""
    query = """
        INSERT INTO DimDate (date, day, month, year, quarter, weekday)
        SELECT 
            date,
            EXTRACT(DAY FROM date) AS day,
            EXTRACT(MONTH FROM date) AS month,
            EXTRACT(YEAR FROM date) AS year,
            EXTRACT(QUARTER FROM date) AS quarter,
            TO_CHAR(date, 'Day') AS weekday
        FROM 
            generate_series('2022-01-01'::date, '2024-12-31'::date, '1 day'::interval) AS date;
    """
    execute_query(cursor, query)
    print("DimDate table populated.")


def populate_dim_user(cursor):
    """Populates the DimUser table."""
    query = """
        INSERT INTO DimUser (user_id, phone_number, username, registration_date, subscription_plan_id, green_user_status_id, is_active, is_staff)
        SELECT 
            user_id,
            phone_number,
            username,
            DATE(registration_date),
            subscription_plan_id,
            green_user_status_id,
            is_active,
            is_staff
        FROM Users;
    """
    execute_query(cursor, query)
    print("DimUser table populated.")


def populate_dim_service_type(cursor):
    """Populates the DimServiceType table."""
    query = """
        INSERT INTO DimServiceType (service_type, service_name)
        VALUES
        ('Deposit', 'Wallet Deposit'),
        ('Withdrawal', 'Wallet Withdrawal'),
        ('Transaction', 'Peer-to-Peer Transfer'),
        ('Bill Payment', 'Utility Bill'),
        ('Merchant Payment', 'Store Purchase'),
        ('Account Subscription', 'Standard/Plus/Premium Subscription'),
        ('Green Subscription', 'Leaf/Tree/Forest Plan');
    """
    execute_query(cursor, query)
    print("DimServiceType table populated.")


def populate_dim_wallet(cursor):
    """Populates the DimWallet table."""
    query = """
        INSERT INTO DimWallet (wallet_id, user_id, balance, is_active, deleted)
        SELECT 
            wallet_id,
            user_id,
            balance,
            is_active,
            deleted
        FROM Wallet;
    """
    execute_query(cursor, query)
    print("DimWallet table populated.")


def populate_fact_transaction(cursor):
    """Populates the FactTransaction table."""
    query = """
        INSERT INTO FactTransaction (transaction_id, date_id, user_id, wallet_id, service_type_id, amount, fees, balance_before, balance_after, transaction_date)
        SELECT 
            T.transaction_id,
            D.date_id,
            U.user_id,
            W.wallet_id,
            S.service_type_id,
            T.amount,
            T.fees,
            T.balance_before,
            T.balance_after,
            T.transaction_date
        FROM 
            Transaction T
        JOIN DimDate D ON D.date = DATE(T.transaction_date)
        JOIN DimUser U ON U.user_id = T.sender_id
        JOIN DimWallet W ON W.wallet_id = T.user_wallet_id
        JOIN DimServiceType S ON S.service_type = T.service_type;
    """
    execute_query(cursor, query)
    print("FactTransaction table populated.")


def close_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()
        print("Database connection closed.")


# Main ELT Pipeline
def main():
    conn = None
    try:
        # Connect to the database
        conn = connect_to_db(DB_CONFIG)
        cursor = conn.cursor()

        # ELT Process
        print("Starting ELT pipeline...")
        populate_dim_date(cursor)
        populate_dim_user(cursor)
        populate_dim_service_type(cursor)
        populate_dim_wallet(cursor)
        populate_fact_transaction(cursor)
        print("ELT pipeline completed successfully.")

    except Exception as e:
        print(f"Error during ELT pipeline: {e}")
    finally:
        # Close the connection
        close_connection(conn)


# Execute the script
if __name__ == "__main__":
    main()
