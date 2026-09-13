import os


def generate_txt_report(data):

    os.makedirs(
        "generated_reports",
        exist_ok=True
    )

    path = (
        "generated_reports/"
        "maintenance_report.txt"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "AI SOFTWARE MAINTENANCE REPORT\n"
        )

        file.write("=" * 40 + "\n\n")

        for key, value in data.items():

            file.write(
                f"{key}: {value}\n\n"
            )

    return path