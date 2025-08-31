import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="finance_db",
        user="postgres",
        password="admin"
    )
    print("Connection to PostgreSQL successful!")
    conn.close()
except Exception as e:
    print("Error connecting to PostgreSQL:", e)
