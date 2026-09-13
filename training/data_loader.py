import pandas as pd

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

TARGET_COLUMN = "Effort"


def load_dataset(path):
    df = pd.read_csv(path)

    missing = [col for col in FEATURE_COLUMNS + [TARGET_COLUMN] if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return df


def get_features_target(df):
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    return X, y