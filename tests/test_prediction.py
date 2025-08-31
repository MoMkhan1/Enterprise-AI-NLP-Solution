
import math
from src.ml.prediction_pipeline import predict_price

def test_predict_price():
    feature = 6
    predicted = predict_price(feature)
    assert math.isclose(predicted, 60, rel_tol=1e-9), f"Expected approximately 60 but got {predicted}"
