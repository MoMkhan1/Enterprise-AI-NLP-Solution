import os
import pandas as pd
from sqlalchemy import create_engine
import logging
import sys

# -----------------------------
# Configure Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# -----------------------------
# Load CSV to PostgreSQL Function
# -----------------------------
def load_csv_to_postgres(
    csv_path: str,
    table_name: str = 'stock_data',
    db_name: str = 'finance_db',
    host: str = 'db',  # Docker service name for PostgreSQL
    user: str = 'postgres',
    password: str = 'admin',
    schema: str = 'public'
) -> bool:
    """
    Load CSV into PostgreSQL with correct headers, adding missing columns if necessary.
    """
    csv_path = os.path.abspath(csv_path)

    if not os.path.exists(csv_path):
        logger.error(f"CSV path invalid: {csv_path}")
        return False

    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}:5432/{db_name}')
        with engine.connect() as conn:
            logger.info(f"Connected to database '{db_name}' on host '{host}'")

        # Read CSV with first row as header
        df = pd.read_csv(csv_path, header=0)
        df.columns = df.columns.str.strip().str.lower()  # normalize

        logger.info(f"Normalized columns: {list(df.columns)}")

        # Add missing columns
        if 'ticker' not in df.columns:
            df['ticker'] = 'DEFAULT'
        if 'date' not in df.columns:
            df['date'] = pd.date_range(end=pd.Timestamp.today(), periods=len(df))

        # Ensure correct column order
        expected_cols = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in expected_cols if col not in df.columns]
        if missing_cols:
            logger.warning(f"Missing columns in CSV: {missing_cols}")

        df = df[expected_cols]

        # Convert datatypes
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Load into PostgreSQL
        df.to_sql(table_name, engine, if_exists='replace', index=False, schema=schema)
        logger.info(f"Loaded {len(df)} rows into table '{table_name}' in database '{db_name}'")
        return True

    except Exception as e:
        logger.error(f"Failed to load CSV '{csv_path}': {e}")
        return False

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    csv_file = os.environ.get("DATA_FILE", "/app/data/finance_data.csv")
    success = load_csv_to_postgres(csv_path=csv_file)
    if not success:
        logger.error("CSV load failed.")
