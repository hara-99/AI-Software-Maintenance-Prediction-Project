import pandas as pd


def clean_data(df):
    df = df.copy()

    df = df.replace([float("inf"), float("-inf")], pd.NA)

    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna()

    return df