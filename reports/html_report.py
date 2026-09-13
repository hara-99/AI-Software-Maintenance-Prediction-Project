import os
import html


def generate_html_report(data):

    os.makedirs(
        "generated_reports",
        exist_ok=True
    )

    path = (
        "generated_reports/"
        "maintenance_report.html"
    )

    content = [
        "<html>",
        "<head>",
        "<title>AI Software Maintenance Report</title>",
        "</head>",
        "<body>",
        "<h1>AI Software Maintenance Report</h1>"
    ]

    for key, value in data.items():

        content.append(
            f"<h2>{html.escape(str(key))}</h2>"
        )

        content.append(
            f"<pre>{html.escape(str(value))}</pre>"
        )

    content.extend([
        "</body>",
        "</html>"
    ])

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(content)
        )

    return path