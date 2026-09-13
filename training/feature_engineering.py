import pandas as pd


def create_features(df):
    df = df.copy()

    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.replace([float("inf"), float("-inf")], pd.NA)
    df = df.fillna(df.median(numeric_only=True))

    return df