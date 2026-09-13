import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }


def evaluate_all_models(models, X_test, y_test):

    results = []

    for name, model in models.items():

        metrics = evaluate_model(
            model,
            X_test,
            y_test
        )

        metrics["Model"] = name

        results.append(metrics)

    return pd.DataFrame(results).sort_values(
        by="RMSE"
    )