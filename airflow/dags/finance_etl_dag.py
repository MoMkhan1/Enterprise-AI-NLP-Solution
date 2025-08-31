"""
Airflow DAG for Finance NLP ETL Pipeline
----------------------------------------
Pipeline steps:
1. Load raw financial CSV data into PostgreSQL
2. Run Spark transformations (feature engineering, aggregation)
3. Apply NLP (sentiment analysis on textual/financial news data)
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging

# Import the ETL functions from your project (make sure these functions exist!)
from src.database.postgres_loader import load_csv_to_postgres
from src.spark.spark_etl import run_spark_etl
from src.nlp.sentiment_analysis import run_sentiment_analysis

# Configure logging for Airflow
logging.basicConfig(level=logging.INFO)

# Define the DAG
with DAG(
    dag_id="finance_nlp_etl",                     # DAG name (shows in Airflow UI)
    description="ETL pipeline: Load data → Spark transform → NLP processing",
    start_date=datetime(2025, 1, 1),              # When to start scheduling
    schedule_interval="@daily",                   # Run daily
    catchup=False,                                # Do not backfill old runs
    tags=["finance", "nlp", "etl"],               # Tags in Airflow UI
) as dag:

    # -----------------------------
    # Task 1: Load CSV → PostgreSQL
    # -----------------------------
    load_data_task = PythonOperator(
        task_id="load_csv_to_postgres",
        python_callable=load_csv_to_postgres,     # Calls your function
    )

    # -----------------------------
    # Task 2: Spark Transformation
    # -----------------------------
    spark_task = PythonOperator(
        task_id="spark_transform",
        python_callable=run_spark_etl,            # Calls your Spark ETL function
    )

    # -----------------------------
    # Task 3: NLP Processing
    # -----------------------------
    nlp_task = PythonOperator(
        task_id="nlp_processing",
        python_callable=run_sentiment_analysis,   # Calls your NLP function
    )

    # -----------------------------
    # Pipeline Flow
    # -----------------------------
    load_data_task >> spark_task >> nlp_task
