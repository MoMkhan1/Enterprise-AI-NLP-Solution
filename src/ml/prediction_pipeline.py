
# src/ml/prediction_pipeline.py

import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_price(feature):
    """
    Dummy ML pipeline: predicts 'price' from 'feature'.
    Replace with real Spark or TensorFlow pipeline later.
    
    Parameters:
    - feature: int or float, the input feature value
    
    Returns:
    - predicted price (float)
    """
    # Sample data
    data = pd.DataFrame({
        "feature": [1, 2, 3, 4, 5],
        "price": [10, 20, 30, 40, 50]
    })

    X = data[["feature"]]
    y = data["price"]

    model = LinearRegression()
    model.fit(X, y)

    next_feature = pd.DataFrame([[feature]], columns=["feature"])
    prediction = model.predict(next_feature)

    return prediction[0]

if __name__ == "__main__":
    predicted_price = predict_price(6)
    print(f"Predicted price for feature=6: {predicted_price:.2f}")

