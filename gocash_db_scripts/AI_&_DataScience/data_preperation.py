import psycopg2
from psycopg2.extras import execute_values
import pandas as pd


DB_CONFIG = {
    "dbname": "demoDB",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}


def connect_to_db(config):
    """Establishes connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        print("Connected Successfully")
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


def close_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()
        print("Database connection closed.")


def pull_data(cursor, query):
    """Pull the necessary data for forecasting and return it as a DataFrame."""

    try:
        cursor.execute(query)
        print("Data pulled successfully")
        # Fetch the results into a pandas DataFrame
        columns = [desc[0] for desc in cursor.description]  # Get column names
        data = cursor.fetchall()  # Fetch all rows
        data_frame = pd.DataFrame(data, columns=columns)
        return data_frame
    except Exception as e:
        print(f"Error during data fetching: {e}")
        raise


def main():
    conn = None
    try:
        # Connect to the database
        print("Start connection process . . . . .")
        conn = connect_to_db(DB_CONFIG)
        cursor = conn.cursor()

        query_1 = """
                    SELECT 
  EXTRACT(YEAR FROM transaction_date) AS year,
  EXTRACT(MONTH FROM transaction_date) AS month,
  EXTRACT(DAY FROM transaction_date) AS day,
  COUNT(*) AS y
FROM 
  transaction
GROUP BY 
  EXTRACT(YEAR FROM transaction_date),
  EXTRACT(MONTH FROM transaction_date),
  EXTRACT(DAY FROM transaction_date)
ORDER BY  
  year,
  month,
  day;
                    """

        query_2 = """
                    SELECT 
  EXTRACT(YEAR FROM registration_date) AS reg_year,
  EXTRACT(MONTH FROM registration_date) AS reg_month,
  EXTRACT(DAY FROM registration_date) AS reg_day,
  COUNT(*) AS total_registered_users
FROM 
  users
GROUP BY 
  EXTRACT(YEAR FROM registration_date),
  EXTRACT(MONTH FROM registration_date),
  EXTRACT(DAY FROM registration_date)
ORDER BY 
  reg_year,
  reg_month,
  reg_day;
                     """

        print("Starting data pulling process")
        reg_users_admin = pull_data(cursor, query_1)
        reg_users_admin.to_csv('total_transactions.csv', index=False)
        print("DataFrame created successfully")
        # print(data_frame)  # Display the DataFrame or perform further operations

        print("End process successfully")

    except Exception as e:
        print(f"Error during pulling data: {e}")
    finally:
        # Close the connection
        close_connection(conn)


if __name__ == "__main__":
    main()
