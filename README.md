# Enterprise AI NLP Solution

## 📌 Overview

This project implements an **Enterprise AI NLP Solution** for financial data analytics with both **batch and real-time capabilities**.  

It features a complete data pipeline that:  
- Ingests data from **PostgreSQL**, **live data sources**, and **Kafka streaming**  
- Processes data with **Apache Spark**  
- Orchestrates workflows using **Airflow**  
- Applies **NLP and ML models**  
- Stores results in **Snowflake**  
- Visualizes insights in **Tableau BI dashboards**

---

## 🔄 Pipeline Flow

**Batch Processing:**  

PostgreSQL → Spark ETL → Airflow DAGs → NLP Models → ML Predictions → Tableau Dashboards


**Real-Time Streaming:**  

Live Data APIs → Kafka Topics → Spark Structured Streaming → Snowflake → NLP Models → ML Predictions → Alerts → Tableau Dashboards


---

## 📂 Project Structure

Enterprise-AI-NLP-Solution/
├── airflow/
│ ├── dags/
│ │ ├── finance_etl_dag.py # Batch ETL pipeline
│ │ ├── load_stock_data_dag.py # PostgreSQL ingestion
│ │ └── streaming_dag.py # Real-time streaming
│ ├── logs/
│ └── plugins/
├── data/
│ └── finance_data.csv # Raw batch data
├── src/
│ ├── nlp/
│ │ ├── sentiment_analysis.py
│ │ ├── document_classifier.py
│ │ └── chatbot_llm.py
│ ├── ml/
│ │ └── prediction_pipeline.py
│ ├── database/
│ │ └── postgres_loader.py
│ ├── spark/
│ │ ├── spark_etl.py
│ │ └── spark_streaming.py
│ ├── streaming/
│ │ ├── kafka_producer.py
│ │ └── kafka_consumer.py
│ └── snowflake/
│ └── snowflake_loader.py
├── tableau/
│ └── finance_dashboards.twbx
├── tests/
│ ├── test_database.py
│ ├── test_spark_etl.py
│ ├── test_nlp_models.py
│ └── test_prediction_pipeline.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/
└── workflows/
└── ci-cd.yml


---

## 🚀 Features

### 1. Data Ingestion
- **Batch:** Load financial data from PostgreSQL  
- **Streaming:** Ingest live stock prices, news, and alerts using Kafka  

### 2. ETL & Stream Processing
- Apache Spark for **batch ETL** (`src/spark/spark_etl.py`)  
- Spark Structured Streaming for **real-time data** (`src/spark/spark_streaming.py`)  

### 3. Workflow Orchestration
- Airflow DAGs for batch + streaming pipelines  

### 4. NLP Models
- Sentiment analysis (`src/nlp/sentiment_analysis.py`)  
- Document classification (`src/nlp/document_classifier.py`)  
- Chatbot/LLM interactions (`src/nlp/chatbot_llm.py`)  

### 5. Machine Learning Predictions
- Real-time and batch ML pipelines for financial predictions  

### 6. BI Dashboards
- Tableau dashboards for **financial insights & alerts**  

### 7. Streaming & Alerts
- Real-time alerts via **email, Slack, or webhooks**  
- Kafka topics:  
  - `stock_prices`  
  - `news_sentiment`  
  - `alerts`  

### 8. Enterprise Storage & Security
- **Snowflake** for secure, scalable cloud storage  
- **Encryption at rest + in transit**  
- **Role-based access control (RBAC)**  
- **Secret management** via Airflow Secrets or Vault  
- **Kafka SSL/SASL** for secure streaming  

---

## ⚙️ Setup & Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Enterprise-AI-NLP-Solution.git
cd Enterprise-AI-NLP-Solution

    Install dependencies:

pip install -r requirements.txt

    Start Docker services:

docker-compose up -d

    Access Airflow UI:
    👉 http://localhost:8080

    Trigger batch & streaming pipelines via Airflow DAGs.

🧪 Running Tests

Run all tests:

pytest tests/

🔄 CI/CD

GitHub Actions (.github/workflows/ci-cd.yml) handles:

    ✅ Linting

    ✅ Unit tests

    ✅ Docker build & deployment

🐳 Docker & Service Management
Start all services

docker-compose up --build -d

Stop and remove everything

docker-compose down -v

View logs

docker logs -f nlp_app
docker logs -f kafka_producer
docker logs -f kafka_consumer
docker logs -f postgres_container

Connect to PostgreSQL inside Docker

docker exec -it postgres_container psql -U postgres -d finance_db

Example SQL:

\dt;
SELECT * FROM transactions LIMIT 10;

🏗 Architecture Diagram

                ┌─────────────┐
                │  Live APIs  │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │   Kafka     │
                │ (Streaming) │
                └──────┬──────┘
                       │
       ┌───────────────┼─────────────────┐
       │               │                 │
┌──────▼──────┐ ┌──────▼──────┐   ┌──────▼──────┐
│ Spark ETL   │ │ Spark Stream│   │   Airflow   │
│ (Batch)     │ │ Processing  │   │ Orchestration │
└──────┬──────┘ └──────┬──────┘   └──────┬──────┘
       │               │                 │
       └──────┬────────┴─────────────────┘
              │
       ┌──────▼──────┐
       │ NLP & ML    │
       │ Models      │
       └──────┬──────┘
              │
       ┌──────▼──────┐
       │ Snowflake   │
       │ (Storage)   │
       └──────┬──────┘
              │
       ┌──────▼──────┐
       │ Tableau BI  │
       │ Dashboards  │
       └─────────────┘

🤝 Contributing

    Fork the repo

    Create feature branch

git checkout -b feature/my-feature

    Commit changes

git commit -am "Add new feature"

    Push branch

git push origin feature/my-feature

    Open Pull Request

📜 License

This project is licensed under the MIT License.
See LICENSE
for details.