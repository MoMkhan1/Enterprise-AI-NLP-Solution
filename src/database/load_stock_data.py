import pandas as pd
from sqlalchemy import create_engine

def load_stock_data():
    # Database credentials
    DB_USER = "postgres"
    DB_PASS = "admin"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "finance_db"

    # Create the database engine
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
  
    # SQL query with "Date" in quotes because it's case-sensitive
    query = 'SELECT * FROM public.stock_data ORDER BY "Date"'

    # Read SQL query results into a Pandas DataFrame
    df = pd.read_sql(query, engine)
    return df

if __name__ == '__main__':
    df = load_stock_data()
    print(df.head())  # Print first few rows to check
