# src/nlp/document_classifier.py

from transformers import pipeline

# Initialize HuggingFace pipeline (using FinBERT or a general BERT for finance tasks)
try:
    document_model = pipeline("text-classification", model="ProsusAI/finbert")
except Exception as e:
    print("⚠️ Could not load FinBERT model, falling back to keyword-based classifier.")
    document_model = None


def classify_financial_document(text: str) -> str:
    """
    Classifies a financial document into categories based on keywords.

    Categories: 'Earnings', 'Mergers', 'Forecasts', 'Others'

    Parameters
    ----------
    text : str

    Returns
    -------
    str : predicted category
    """
    text = text.lower()

    if "revenue" in text or "profit" in text:
        return "Earnings"
    elif "acquisition" in text or "merger" in text:
        return "Mergers"
    elif "guidance" in text or "forecast" in text:
        return "Forecasts"
    else:
        return "Others"


def classify_document(text: str) -> dict:
    """
    Uses transformer model (FinBERT) if available, 
    otherwise falls back to keyword-based classification.
    """
    if document_model:
        result = document_model(text, truncation=True, max_length=512)
        return {"label": result[0]["label"], "score": float(result[0]["score"])}
    else:
        # Fallback to keyword classification
        return {"label": classify_financial_document(text), "score": 0.90}


if __name__ == "__main__":
    docs = [
        "The company announced strong revenue and profit for Q3 2025.",
        "TechCorp finalized a merger with SoftSolutions.",
        "The bank issued new guidance for next quarter.",
        "Investors are uncertain about market conditions."
    ]

    for doc in docs:
        result = classify_document(doc)
        print(f"\n📄 Document: {doc}")
        print(f"🔎 Predicted Category: {result['label']} (Confidence: {result['score']:.2f})")
