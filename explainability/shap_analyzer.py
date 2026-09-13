import joblib
import pandas as pd
import shap


FEATURE_COLUMNS = [
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


def explain_prediction(features):

    model = joblib.load(
        "models/stacking_ensemble.pkl"
    )

    data = pd.DataFrame(
        [[features.get(c, 0) for c in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS
    )

    try:

        explainer = shap.Explainer(model)

        shap_values = explainer(data)

        values = shap_values.values[0]

        explanation = []

        for name, value in zip(
            FEATURE_COLUMNS,
            values
        ):
            explanation.append({
                "feature": name,
                "impact": float(value)
            })

        explanation.sort(
            key=lambda x: abs(x["impact"]),
            reverse=True
        )

        return explanation

    except Exception as error:

        return [{
            "feature": "SHAP",
            "impact": 0,
            "error": str(error)
        }]