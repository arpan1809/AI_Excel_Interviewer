import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import re

REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

def safe_text(text):
    """Sanitize text and split long words"""
    text = str(text)
    text = re.sub(r'(\S{50,})', lambda m: ' '.join([m.group(0)[i:i+50] for i in range(0, len(m.group(0)), 50)]), text)
    return text

def generate_report(candidate_name, questions, answers, evaluations):
    """
    Generate a PDF report using ReportLab
    Returns the path to the saved PDF
    """
    filename = f"{candidate_name.replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(REPORT_FOLDER, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='HeadingCenter', alignment=1, fontSize=16, spaceAfter=10, leading=20))
    styles.add(ParagraphStyle(name='SubHeading', fontSize=12, spaceAfter=6, leading=15))
    styles.add(ParagraphStyle(name='NormalJustify', fontSize=11, leading=14))

    story = []

    
    story.append(Paragraph("Excel Mock Interview Report", styles['HeadingCenter']))
    story.append(Spacer(1, 12))

    
    story.append(Paragraph(f"<b>Candidate:</b> {safe_text(candidate_name)}", styles['NormalJustify']))
    story.append(Paragraph(f"<b>Topic:</b> Excel Interview", styles['NormalJustify']))
    story.append(Paragraph(f"<b>Date:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles['NormalJustify']))
    story.append(Spacer(1, 12))

    
    data = [["Q #", "Score (0-10)"]]
    total_score = 0
    for i, eval in enumerate(evaluations):
        score = eval.get("score", 0)
        total_score += score
        data.append([str(i+1), str(score)])
    avg_score = round(total_score / len(evaluations), 2) if evaluations else 0
    table = Table(data, hAlign='LEFT', colWidths=[50, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ]))
    story.append(table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"<b>Average Score:</b> {avg_score} / 10", styles['NormalJustify']))
    story.append(Spacer(1, 12))

    
    story.append(Paragraph("Detailed Responses", styles['SubHeading']))
    story.append(Spacer(1, 6))

    for i, (q, a, eval) in enumerate(zip(questions, answers, evaluations)):
        question_text = q['question'] if isinstance(q, dict) else q
        answer_text = a if a.strip() else "No Answer"
        score_text = eval.get("score", 0)
        feedback_text = eval.get("feedback", "No feedback")

        story.append(Paragraph(f"<b>Q{i+1}:</b> {safe_text(question_text)}", styles['NormalJustify']))
        story.append(Paragraph(f"<b>Answer:</b> {safe_text(answer_text)}", styles['NormalJustify']))
        story.append(Paragraph(f"<b>Score:</b> {safe_text(str(score_text))}", styles['NormalJustify']))
        story.append(Paragraph(f"<b>Feedback:</b> {safe_text(feedback_text)}", styles['NormalJustify']))
        story.append(Spacer(1, 8))

    doc.build(story)
    return filepath

