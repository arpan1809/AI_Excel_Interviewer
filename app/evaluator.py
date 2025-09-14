import os
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def get_headers():
    """Return the latest Groq API key dynamically."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set in environment")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def call_groq(prompt: str, max_tokens: int = 400, temperature: float = 0.3, retries: int = 4):
    """
    Call Groq API with retry + backoff to handle rate limits.
    """
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    for attempt in range(retries):
        try:
            resp = requests.post(GROQ_API_URL, headers=get_headers(), json=payload)
            if resp.status_code == 429:  # rate limited
                wait = min(2 ** attempt, 20)
                print(f"⚠️ Rate limited, retrying in {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"⚠️ Groq API error: {e}")
            time.sleep(1)

    raise RuntimeError("Groq API failed after retries")




def evaluate_answers_batch(questions, answers, batch_size: int = 5):
    """
    Evaluate answers in small batches using Groq.
    Returns list of dicts: {"score": 0-10, "feedback": "constructive feedback"}
    """
    results = []

    for i in range(0, len(questions), batch_size):
        sub_qs = questions[i:i+batch_size]
        sub_as = answers[i:i+batch_size]

        
        sub_as = [a if len(a.split()) < 50 else " ".join(a.split()[:50]) + " ..." for a in sub_as]

        qa_text = "\n".join(
            [f"Q{i+j+1}: {q if isinstance(q, str) else q['question']}\nA{i+j+1}: {a if a.strip() else 'No Answer'}"
             for j, (q, a) in enumerate(zip(sub_qs, sub_as))]
        )

        prompt = f"""
You are an expert Excel interviewer.
Evaluate the following Q&A strictly and return JSON ONLY:

Return a JSON array of objects, one per question:
[{{"score": int (0-10), "feedback": "constructive feedback"}}...]

Transcript:
{qa_text}

Instructions:
- Give a score from 0 to 10.
- Feedback must be specific to the answer.
- Do not include any extra text outside JSON.
"""

        try:
            text = call_groq(prompt, max_tokens=600, temperature=0.2)

            
            try:
                sub_results = json.loads(text)
            except json.JSONDecodeError:
                
                fixed_text = text.replace("'", '"')
                sub_results = json.loads(fixed_text)

            if isinstance(sub_results, list) and all("score" in r and "feedback" in r for r in sub_results):
                results.extend(sub_results)
            else:
                raise ValueError("Invalid response structure")
        except Exception as e:
            print("⚠️ Evaluation failed, generating minimal fallback:", e)
            
            
            for q, a in zip(sub_qs, sub_as):
                feedback = "No answer provided" if not a.strip() else "Answer needs improvement"
                results.append({"score": 0 if not a.strip() else 3, "feedback": feedback})

    return results
