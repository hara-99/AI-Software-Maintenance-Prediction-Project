import os
import joblib
from catboost import CatBoostRegressor


def train_catboost(X_train, y_train):
    model = CatBoostRegressor(
        iterations=300,
        learning_rate=0.05,
        depth=6,
        loss_function="RMSE",
        verbose=False,
        random_seed=42
    )

    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/catboost.pkl")

    return model