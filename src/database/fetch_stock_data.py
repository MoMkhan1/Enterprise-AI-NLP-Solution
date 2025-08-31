from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:admin@localhost:5432/finance_db')

with engine.connect() as conn:
    # Removed ORDER BY Date since no Date column exists
    query = text("SELECT * FROM public.stock_data LIMIT 5;")
    result = conn.execute(query).fetchall()
    for row in result:
        print(row)
