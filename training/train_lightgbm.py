import os
import joblib
from lightgbm import LGBMRegressor


def train_lightgbm(X_train, y_train):
    model = LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=-1,
        num_leaves=31,
        random_state=42,
        verbosity=-1
    )

    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/lightgbm.pkl")

    return model