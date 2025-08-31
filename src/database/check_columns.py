from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:admin@localhost:5432/finance_db')

with engine.connect() as conn:
    columns = conn.execute(text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'stock_data' AND table_schema = 'public';
    """)).fetchall()
    print("Columns in stock_data table:", [col[0] for col in columns])
