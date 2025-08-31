"""
Stock Data ETL with Sentiment Analysis
--------------------------------------
This module:
1. Loads CSV financial data into PostgreSQL.
2. Performs sentiment analysis using DistilBERT on a text column.
3. Inserts enriched data into PostgreSQL.
4. Can be used as a standalone script or Airflow task.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
import logging
from transformers import pipeline, AutoTokenizer, TFAutoModelForSequenceClassification

# -----------------------------
# Configure logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Initialize DistilBERT Sentiment Pipeline
# -----------------------------
def init_sentiment_pipeline():
    """
    Initialize the DistilBERT sentiment analysis pipeline (TensorFlow version).
    """
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        framework="tf"
    )
    return sentiment_analyzer

# -----------------------------
# Analyze sentiment for a text column
# -----------------------------
def analyze_sentiment_column(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """
    Apply sentiment analysis to a dataframe column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    text_column : str
        Column containing text to analyze

    Returns
    -------
    pd.DataFrame
        Dataframe with added 'Sentiment_Label' and 'Sentiment_Score'
    """
    if text_column not in df.columns:
        logger.warning(f"Text column '{text_column}' not found in DataFrame. Skipping sentiment analysis.")
        return df

    sentiment_analyzer = init_sentiment_pipeline()
    logger.info(f"Running sentiment analysis on column '{text_column}'...")
    
    results = df[text_column].apply(lambda x: sentiment_analyzer(str(x))[0])
    df['Sentiment_Label'] = results.apply(lambda x: x['label'])
    df['Sentiment_Score'] = results.apply(lambda x: x['score'])

    logger.info("Sentiment analysis completed.")
    return df

# -----------------------------
# Load CSV into PostgreSQL
# -----------------------------
def load_csv_to_postgres(csv_path: str = None, table_name: str = 'stock_data', text_column: str = None) -> bool:
    """
    Load CSV data into PostgreSQL with optional sentiment analysis.

    Parameters
    ----------
    csv_path : str
        Path to CSV file. Defaults to env variable CSV_PATH or /app/data/finance_data.csv
    table_name : str
        Target table name in PostgreSQL
    text_column : str
        Optional column to run sentiment analysis on
    """
    csv_path = csv_path or os.getenv('CSV_PATH', './data/finance_data.csv')
    db_config = {
        'db_name': os.getenv('DB_NAME', 'finance_db'),
        'db_user': os.getenv('DB_USER', 'postgres'),
        'db_pass': os.getenv('DB_PASS', 'admin'),
        'db_host': os.getenv('DB_HOST', 'localhost'),
        'db_port': os.getenv('DB_PORT', '5432')
    }

    if not os.path.exists(csv_path):
        logger.error(f"CSV file not found at {csv_path}")
        return False

    try:
        df = pd.read_csv(csv_path)
        logger.info(f"Initial data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

        # Rename 'Adj Close' to 'Price' if exists
        if 'Adj Close' in df.columns:
            df.rename(columns={'Adj Close': 'Price'}, inplace=True)

        # Convert date and numeric columns
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        numeric_cols = ['Price', 'Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NaN in required columns
        required_cols = ['Date'] + [col for col in numeric_cols if col in df.columns]
        df.dropna(subset=required_cols, inplace=True)
        logger.info(f"Data after cleaning: {df.shape[0]} rows")

        # Add unique ID
        if 'id' not in df.columns:
            df.insert(0, 'id', range(1, len(df) + 1))

        # Run sentiment analysis if column specified
        if text_column:
            df = analyze_sentiment_column(df, text_column)

        # Connect to PostgreSQL
        conn_str = (
            f"postgresql://{db_config['db_user']}:{db_config['db_pass']}@"
            f"{db_config['db_host']}:{db_config['db_port']}/{db_config['db_name']}"
        )
        engine = create_engine(conn_str)

        # Insert into PostgreSQL
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logger.info(f"✅ Data inserted into '{table_name}' successfully!")

        return True

    except Exception as e:
        logger.exception(f"Error loading CSV to Postgres: {e}")
        return False

# -----------------------------
# Airflow ETL Task Wrapper
# -----------------------------
def etl_task(**kwargs):
    """
    Wrapper for Airflow PythonOperator.
    """
    csv_path = kwargs.get('csv_path')
    table_name = kwargs.get('table_name', 'stock_data')
    text_column = kwargs.get('text_column', 'NewsHeadline')  # default column for sentiment

    success = load_csv_to_postgres(csv_path, table_name, text_column)
    if not success:
        raise Exception("Stock CSV to PostgreSQL ETL failed")
    return "ETL Completed Successfully"

# -----------------------------
# Direct execution
# -----------------------------
if __name__ == "__main__":
    # Default execution with optional sentiment column
    load_csv_to_postgres(text_column='NewsHeadline')
