from reports.pdf_report import generate_pdf_report
from reports.docx_report import generate_docx_report
from reports.excel_report import generate_excel_report
from reports.csv_report import generate_csv_report
from reports.html_report import generate_html_report
from reports.json_report import generate_json_report
from reports.txt_report import generate_txt_report


def generate_all_reports(data):

    files = {}

    files["PDF"] = generate_pdf_report(data)
    files["DOCX"] = generate_docx_report(data)
    files["XLSX"] = generate_excel_report(data)
    files["CSV"] = generate_csv_report(data)
    files["HTML"] = generate_html_report(data)
    files["JSON"] = generate_json_report(data)
    files["TXT"] = generate_txt_report(data)

    return files