import os
import joblib
from sklearn.linear_model import LinearRegression


def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/linear_regression.pkl")

    return model