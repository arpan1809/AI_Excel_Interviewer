import re
from app.evaluator import call_groq


def generate_first_question():
    """
    Generate a good starting question (beginner/intermediate Excel).
    """
    prompt = """
You are an Excel interviewer.
Ask the first question to a candidate. 
It should be a simple but insightful Excel question (e.g., formulas, formatting, data handling).
Return only the question text, no explanations.
"""
    text = call_groq(prompt, max_tokens=80, temperature=0.7).strip()
    return clean_question(text)


def generate_followup_question(prev_q, prev_a, difficulty="medium", asked_so_far=None):
    """
    Generate a follow-up question based on candidate's last answer.
    Difficulty should increase/decrease depending on answer quality.
    """
    asked_so_far = asked_so_far or []

    prompt = f"""
You are an Excel interviewer.
The last question was: "{prev_q}"
The candidate answered: "{prev_a}"

Now generate ONE new Excel interview question that follows up naturally.
Difficulty should be {difficulty}.
Do not repeat previous questions. 
Return only the question text, no answers, no numbering.
"""
    text = call_groq(prompt, max_tokens=100, temperature=0.7).strip()
    q = clean_question(text)

    
    if q in asked_so_far:
        q = f"{q} (rephrased)"
    return q


def clean_question(text):
    """Strip unwanted numbering/bullets."""
    return re.sub(r"^\s*\d+[\.\)]\s*", "", text).strip()
