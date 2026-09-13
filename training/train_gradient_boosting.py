import os
import joblib
from sklearn.ensemble import GradientBoostingRegressor


def train_gradient_boosting(X_train, y_train):
    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )

    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/gradient_boosting.pkl")

    return model