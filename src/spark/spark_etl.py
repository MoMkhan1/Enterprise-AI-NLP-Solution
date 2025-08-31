def run_spark_etl():
    """
    Transform step: Run Spark ETL pipeline.
    Example: read from Postgres, clean/aggregate, and write back to Postgres.
    Airflow will call this function as Task 2.
    """
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder \
        .appName("FinanceSparkETL") \
        .getOrCreate()
    
    # Example: read from Postgres
    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://db:5432/finance_db") \
        .option("dbtable", "stock_data") \
        .option("user", "postgres") \
        .option("password", "admin") \
        .load()
    
    # Example transformation: calculate average close price per year
    df_transformed = df.groupBy("year").avg("Close")
    
    # Save back to Postgres
    df_transformed.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://db:5432/finance_db") \
        .option("dbtable", "stock_data_transformed") \
        .option("user", "postgres") \
        .option("password", "admin") \
        .mode("overwrite") \
        .save()
    
    spark.stop()
    print("✅ Spark ETL completed successfully")
