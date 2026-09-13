import os
import pandas as pd


def generate_excel_report(data):

    os.makedirs(
        "generated_reports",
        exist_ok=True
    )

    path = (
        "generated_reports/"
        "maintenance_report.xlsx"
    )

    rows = []

    for key, value in data.items():

        rows.append({
            "Field": key,
            "Value": str(value)
        })

    df = pd.DataFrame(rows)

    with pd.ExcelWriter(
        path,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Report"
        )

    return path