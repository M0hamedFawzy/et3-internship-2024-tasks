import psycopg2

# Database configuration
DB_CONFIG = {
    "dbname": "DWBI",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}


def update_is_active(table, limit, id_):
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Prepare the SQL query
        query = f"""
        UPDATE {table}
        SET service_type_id = 4
        WHERE {id_} IN (
            SELECT {id_} FROM {table}
            ORDER BY {id_} ASC
            LIMIT %s
        );
        """

        # Execute the query
        cursor.execute(query, (limit,))
        conn.commit()

        print(f"Successfully updated {limit} rows in {table}.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Update dimuser
    update_is_active("facttransaction", 3374, "transaction_id")

    # Update dimwallet
    # update_is_active("dimwallet", 7106, "wallet_id")
