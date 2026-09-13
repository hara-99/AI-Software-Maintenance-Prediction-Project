import os
import joblib
from sklearn.ensemble import RandomForestRegressor


def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/random_forest.pkl")

    return model