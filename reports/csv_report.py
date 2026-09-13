import os
import pandas as pd


def generate_csv_report(data):

    os.makedirs(
        "generated_reports",
        exist_ok=True
    )

    path = (
        "generated_reports/"
        "maintenance_report.csv"
    )

    rows = []

    for key, value in data.items():

        rows.append({
            "Field": key,
            "Value": str(value)
        })

    pd.DataFrame(rows).to_csv(
        path,
        index=False
    )

    return path