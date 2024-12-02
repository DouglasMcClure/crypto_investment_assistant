from sklearn.linear_model import LinearRegression
import numpy as np

def predict_prices(real_time_prices):
    """
    Predict the next price using a simple linear regression model with real-time data.
    """
    if len(real_time_prices) < 5:  # Ensure enough data for predictions
        return None

    # Prepare the training data
    X = np.arange(len(real_time_prices)).reshape(-1, 1)
    y = np.array(real_time_prices).reshape(-1, 1)

    # Fit a simple linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict the next price
    next_day = np.array([[len(real_time_prices)]])  # The next time step
    predicted_price = model.predict(next_day)

    return predicted_price
