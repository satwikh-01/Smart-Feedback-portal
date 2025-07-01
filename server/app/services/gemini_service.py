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

def suggest_tags_for_feedback(text: str) -> list[str]:
    """
    Suggests relevant tags based on the feedback content.
    """
    prompt = (
        "Based on the following feedback content, suggest up to 3 relevant tags "
        "from this list: [Leadership, Communication, Teamwork, Technical Skills, "
        "Problem Solving, Creativity, Time Management, Adaptability]. "
        "Return only a comma-separated list of the tag names. "
        f"Content: '{text}'"
    )
    response = model.generate_content(prompt)
    tags = [tag.strip() for tag in response.text.split(',')]
    return tags

def generate_comprehensive_feedback(strengths: str, areas_for_improvement: str) -> str:
    """
    Generates a well-rounded feedback message from bullet points.
    """
    prompt = (
        "Based on the following points, write a comprehensive and constructive feedback paragraph. "
        "The tone should be professional, balanced, and encouraging. "
        f"Strengths: '{strengths}'. Areas for Improvement: '{areas_for_improvement}'"
    )
    response = model.generate_content(prompt)
    return response.text

def analyze_sentiment(text: str) -> str:
    """
    Analyzes the sentiment of the feedback text.
    """
    prompt = (
        "Analyze the overall sentiment of the following feedback text. "
        "Respond with only one word: 'positive', 'neutral', or 'negative'. "
        f"Text: '{text}'"
    )
    response = model.generate_content(prompt)
    return response.text.lower().strip()
