
from src.nlp.sentiment_analysis import analyze_sentiment

def test_positive_sentiment():
    result = analyze_sentiment("I love this product!")
    assert result['label'] == "POSITIVE"

def test_negative_sentiment():
    result = analyze_sentiment("This is the worst experience ever.")
    assert result['label'] == "NEGATIVE"

