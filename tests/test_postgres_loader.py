
# tests/test_postgres_loader.py

import os
import pytest
from src.database.postgres_loader import load_csv_to_postgres

def test_load_csv_to_postgres_runs():
    # Prepare a minimal CSV path and db config (adjust paths for your environment)
    csv_path = os.path.join(os.path.dirname(__file__), '../data/finance_data.csv')

    # Use test DB config - make sure this is a test DB or a mock DB in real scenario
    db_config = {
        'db_name': 'finance_db',
        'db_user': 'postgres',
        'db_pass': 'admin',
        'db_host': 'localhost',
        'db_port': '5432'
    }
    
    # Just test if the function runs without error
    load_csv_to_postgres(csv_path, db_config)
