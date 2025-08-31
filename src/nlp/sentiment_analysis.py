"""
Sentiment Analysis Module (DistilBERT-based)
--------------------------------------------
Analyze text sentiment in single or batch mode with logging.
"""

import logging
import pandas as pd
from transformers import pipeline, AutoTokenizer, TFAutoModelForSequenceClassification
import os

# -----------------------------
# Ensure Logs Folder Exists
# -----------------------------
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# -----------------------------
# Logging Configuration
# -----------------------------
LOG_FILE = os.path.join(LOGS_DIR, "sentiment_analysis.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Load Model & Tokenizer Once
# -----------------------------
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
logger.info(f"Loading model: {MODEL_NAME}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = TFAutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer,
    framework="tf"
)

# -----------------------------
# Single Text Sentiment
# -----------------------------
def analyze_sentiment(text: str) -> dict:
    result = sentiment_analyzer(text)[0]
    logger.info(f"Input: {text} | Result: {result}")
    return result

# -----------------------------
# Batch Mode (ETL)
# -----------------------------
def run_sentiment_analysis():
    texts = [
        "The financial outlook is extremely positive!",
        "Investors are worried about the potential market crash.",
        "Earnings reports exceeded expectations."
    ]
    results = sentiment_analyzer(texts)
    df = pd.DataFrame({"text": texts, "sentiment": results})
    
    logger.info("Batch Sentiment Analysis Results:\n%s", df.to_string(index=False))
    print("✅ Sentiment analysis completed.")
    return df

# -----------------------------
# Main (Standalone Test)
# -----------------------------
if __name__ == "__main__":
    sample = "The market is showing strong growth today."
    result = analyze_sentiment(sample)
    print(f"Text: {sample}")
    print(f"Sentiment: {result['label']} ({result['score']:.4f})")
    run_sentiment_analysis()
