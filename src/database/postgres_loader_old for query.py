import pandas as pd
from sqlalchemy import create_engine
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_csv_to_postgres(csv_path, db_config, table_name='stock_data'):
    if not os.path.exists(csv_path):
        logging.error(f"CSV file not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    logging.info(f"Initial data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # Rename 'Adj Close' to 'Price'
    if 'Adj Close' in df.columns:
        df.rename(columns={'Adj Close': 'Price'}, inplace=True)

    # Add unique id
    df.insert(0, 'id', range(1, len(df) + 1))

    # Convert numeric columns
    numeric_cols = ['Price', 'Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Optional: drop rows with all NaNs in numeric columns
    df.dropna(subset=[col for col in numeric_cols if col in df.columns], how='all', inplace=True)
    logging.info(f"Data after cleaning: {df.shape[0]} rows")

    conn_str = (
        f"postgresql://{db_config['db_user']}:{db_config['db_pass']}@"
        f"{db_config['db_host']}:{db_config['db_port']}/{db_config['db_name']}"
    )
    engine = create_engine(conn_str)

    df.to_sql(table_name, engine, if_exists='replace', index=False)
    logging.info(f"✅ Data inserted into '{table_name}' successfully!")

# Example run
if __name__ == "__main__":
    csv_file_path = r'F:\GITHUB\Enterprise-AI-NLP-Solution\data\finance_data.csv'
    database_config = {
        'db_name': 'finance_db',
        'db_user': 'postgres',
        'db_pass': 'admin',
        'db_host': 'localhost',
        'db_port': '5432'
    }
    load_csv_to_postgres(csv_file_path, database_config)
