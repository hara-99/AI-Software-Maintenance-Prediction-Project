import os

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf_report(data):

    os.makedirs(
        "generated_reports",
        exist_ok=True
    )

    path = (
        "generated_reports/"
        "maintenance_report.pdf"
    )

    document = SimpleDocTemplate(
        path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "AI Software Maintenance Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    for key, value in data.items():

        elements.append(
            Paragraph(
                str(key),
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                str(value).replace(
                    "\n",
                    "<br/>"
                ),
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

    document.build(elements)

    return path