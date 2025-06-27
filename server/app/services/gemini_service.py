import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_feedback_suggestion(prompt: str) -> str:
    """
    Generates feedback content based on a manager's prompt.
    """
    full_prompt = (
        "Based on the following points, write a constructive feedback paragraph for an employee. "
        "The tone should be professional and encouraging. The points are: "
        f"'{prompt}'"
    )
    response = model.generate_content(full_prompt)
    return response.text

def rephrase_text(text: str) -> str:
    """
    Rephrases the given text to be more clear and professional.
    """
    prompt = (
        "Rephrase the following text to be more professional, clear, and constructive, "
        "while retaining the core message. Here is the text: "
        f"'{text}'"
    )
    response = model.generate_content(prompt)
    return response.text

def suggest_tags_for_feedback(strengths: str, areas_for_improvement: str) -> list[str]:
    """
    Suggests relevant tags based on the feedback content.
    """
    content = f"Strengths: {strengths}. Areas for improvement: {areas_for_improvement}."
    prompt = (
        "Based on the following feedback content, suggest up to 3 relevant tags "
        "from this list: [Leadership, Communication, Teamwork, Technical Skills, "
        "Problem Solving, Creativity, Time Management, Adaptability]. "
        "Return only a comma-separated list of the tag names. "
        f"Content: '{content}'"
    )
    response = model.generate_content(prompt)
    tags = [tag.strip() for tag in response.text.split(',')]
    return tags