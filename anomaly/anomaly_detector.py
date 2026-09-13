import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "isolation_forest.pkl"
)


def train_anomaly_model(
    training_features
):

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    model.fit(
        training_features
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    return model


def detect_anomaly(
    features
):

    if not os.path.exists(
        MODEL_PATH
    ):

        return {
            "status": "Model not trained",
            "is_anomaly": False,
            "score": 0.0
        }

    model = joblib.load(
        MODEL_PATH
    )

    array = np.array(
        features,
        dtype=float
    ).reshape(
        1,
        -1
    )

    prediction = model.predict(
        array
    )[0]

    score = model.decision_function(
        array
    )[0]

    return {
        "status": "Anomaly" if prediction == -1 else "Normal",
        "is_anomaly": prediction == -1,
        "score": float(score)
    }