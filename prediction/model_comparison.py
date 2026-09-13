import pandas as pd


def load_model_comparison():

    path = "analysis_results/model_comparison.csv"

    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame()