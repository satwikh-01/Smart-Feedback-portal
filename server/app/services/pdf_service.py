from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from typing import List, Dict, Any
import datetime

# The import for the SQLAlchemy Feedback model is no longer needed.
# from app.models.feedback import Feedback

def parse_iso_datetime(iso_str: str) -> datetime.datetime:
    """Helper function to parse ISO 8601 datetime strings from Supabase."""
    # Supabase may include a timezone offset with '+', which fromisoformat can handle in Python 3.11+
    # For broader compatibility, we can strip it if it exists.
    if '+' in iso_str:
        iso_str = iso_str.split('+')[0]
    return datetime.datetime.fromisoformat(iso_str)


def create_feedback_pdf(feedback_list: List[Dict[str, Any]]) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for feedback in feedback_list:
        # Use dictionary key access for all fields
        employee_name = feedback.get('employee', {}).get('full_name', 'N/A')
        story.append(Paragraph(f"Feedback Report for: {employee_name}", styles['h1']))
        story.append(Spacer(1, 12))

        created_at_str = "N/A"
        if feedback.get('created_at'):
            created_at_dt = parse_iso_datetime(feedback['created_at'])
            created_at_str = created_at_dt.strftime('%Y-%m-%d')
            
        manager_name = feedback.get('manager', {}).get('full_name', 'N/A')
        sentiment = (feedback.get('sentiment') or 'N/A').title()

        story.append(Paragraph(f"<b>Date:</b> {created_at_str}", styles['Normal']))
        story.append(Paragraph(f"<b>Manager:</b> {manager_name}", styles['Normal']))
        story.append(Paragraph(f"<b>Sentiment:</b> {sentiment}", styles['Normal']))
        story.append(Spacer(1, 24))

        story.append(Paragraph("Strengths", styles['h2']))
        story.append(Paragraph(feedback.get('strengths') or "N/A", styles['BodyText']))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Areas for Improvement", styles['h2']))
        story.append(Paragraph(feedback.get('areas_for_improvement') or "N/A", styles['BodyText']))
        story.append(Spacer(1, 24))

        if feedback.get('comments'):
            story.append(Paragraph("Comments", styles['h2']))
            for comment in feedback['comments']:
                commenter_name = comment.get('user', {}).get('full_name', 'Unknown User')
                comment_created_at_str = "some time"
                if comment.get('created_at'):
                    comment_created_at_dt = parse_iso_datetime(comment['created_at'])
                    comment_created_at_str = comment_created_at_dt.strftime('%Y-%m-%d')
                
                story.append(Paragraph(f"<i>{commenter_name} on {comment_created_at_str}:</i>", styles['Italic']))
                story.append(Paragraph(comment.get('content', ''), styles['BodyText']))
                story.append(Spacer(1, 6))

        story.append(PageBreak())

    doc.build(story)
    buffer.seek(0)
    return buffer