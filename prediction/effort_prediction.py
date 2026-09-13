import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "stacking_ensemble.pkl"
)


FEATURE_NAMES = [
    "N_effort",
    "Enquiry",
    "Interface",
    "File",
    "Input",
    "AFP",
    "Added",
    "Duration",
    "PDR_AFP",
    "Output"
]


def predict_effort(
    values
):

    if not os.path.exists(
        MODEL_PATH
    ):

        raise FileNotFoundError(
            "stacking_ensemble.pkl not found. "
            "Run training first."
        )

    model = joblib.load(
        MODEL_PATH
    )

    row = [
        float(
            values[feature]
        )
        for feature in FEATURE_NAMES
    ]

    dataframe = pd.DataFrame(
        [row],
        columns=FEATURE_NAMES
    )

    prediction = model.predict(
        dataframe
    )

    return float(
        prediction[0]
    )