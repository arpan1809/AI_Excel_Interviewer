from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def create_pdf_report(topic, questions, answers, evaluations, filename="reports/interview_report.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    elements.append(Paragraph(f"<b>{topic} Interview Report</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    for i, (q, a, e) in enumerate(zip(questions, answers, evaluations), 1):
        elements.append(Paragraph(f"<b>Q{i}:</b> {q}", styles["Heading3"]))
        elements.append(Paragraph(f"<b>Answer:</b> {a}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Evaluation:</b> {e}", styles["Normal"]))
        elements.append(Spacer(1, 15))

    doc.build(elements)
    return filename
