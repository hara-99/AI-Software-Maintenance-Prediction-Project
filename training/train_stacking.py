import os
import joblib

from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor


def train_stacking(X_train, y_train):

    estimators = [
        (
            "random_forest",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            )
        ),
        (
            "gradient_boosting",
            GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.05,
                random_state=42
            )
        ),
        (
            "xgboost",
            XGBRegressor(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=5,
                objective="reg:squarederror",
                random_state=42
            )
        ),
        (
            "lightgbm",
            LGBMRegressor(
                n_estimators=200,
                learning_rate=0.05,
                random_state=42,
                verbosity=-1
            )
        ),
        (
            "catboost",
            CatBoostRegressor(
                iterations=200,
                learning_rate=0.05,
                depth=6,
                verbose=False,
                random_seed=42
            )
        )
    ]

    model = StackingRegressor(
        estimators=estimators,
        final_estimator=Ridge(alpha=1.0),
        cv=5,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/stacking_ensemble.pkl")

    return model