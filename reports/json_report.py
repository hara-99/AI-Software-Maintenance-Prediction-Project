import json
import os


def generate_json_report(data):

    os.makedirs(
        "generated_reports",
        exist_ok=True
    )

    path = (
        "generated_reports/"
        "maintenance_report.json"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            default=str
        )

    return path