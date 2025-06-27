from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from app.models.feedback import Feedback
from typing import List

def create_feedback_pdf(feedback_list: List[Feedback]) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for feedback in feedback_list:
        story.append(Paragraph(f"Feedback Report for: {feedback.employee.full_name}", styles['h1']))
        story.append(Spacer(1, 12))

        story.append(Paragraph(f"<b>Date:</b> {feedback.created_at.strftime('%Y-%m-%d')}", styles['Normal']))
        story.append(Paragraph(f"<b>Manager:</b> {feedback.manager.full_name}", styles['Normal']))
        story.append(Paragraph(f"<b>Sentiment:</b> {feedback.sentiment.value.title()}", styles['Normal']))
        story.append(Spacer(1, 24))

        story.append(Paragraph("Strengths", styles['h2']))
        story.append(Paragraph(feedback.strengths or "N/A", styles['BodyText']))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Areas for Improvement", styles['h2']))
        story.append(Paragraph(feedback.areas_for_improvement or "N/A", styles['BodyText']))
        story.append(Spacer(1, 24))

        if feedback.comments:
            story.append(Paragraph("Comments", styles['h2']))
            for comment in feedback.comments:
                story.append(Paragraph(f"<i>{comment.user.full_name} on {comment.created_at.strftime('%Y-%m-%d')}:</i>", styles['Italic']))
                story.append(Paragraph(comment.content, styles['BodyText']))
                story.append(Spacer(1, 6))

        story.append(PageBreak())

    doc.build(story)
    buffer.seek(0)
    return buffer