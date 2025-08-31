from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.database.postgres_loader import load_data  # make sure load_data() is the main function

# DAG definition
with DAG(
    dag_id='load_stock_data',
    start_date=datetime(2025, 8, 17),
    schedule_interval='@daily',  # run daily
    catchup=False,
    tags=['finance', 'postgres']
) as dag:

    load_task = PythonOperator(
        task_id='load_stock_data_task',
        python_callable=load_data
    )
