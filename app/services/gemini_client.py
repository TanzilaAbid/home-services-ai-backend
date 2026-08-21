import os
import json
import requests
 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)
 
 
def call_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini 2.5 Flash and returns the raw text response.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in .env")
 
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
 
    response = requests.post(GEMINI_URL, headers=headers, params=params, json=body, timeout=60)
    response.raise_for_status()
    data = response.json()
 
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise ValueError(f"Unexpected Gemini response format: {data}")
 
 
def extract_intent(user_message: str) -> dict:
    """
    Asks Gemini to pull structured info out of a free-text customer message.
    e.g. "I need a painter for my 3-bedroom house next Tuesday under $300"
    -> {"category": "painter", "budget_max": 300, "date_requested": "...", "location": null}
    """
    prompt = f"""
Extract structured booking information from this customer message.
Return ONLY valid JSON, no markdown, no explanation, in this exact format:
{{
  "category": "painter|plumber|electrician|null",
  "budget_max": number or null,
  "date_requested": "YYYY-MM-DD or description or null",
  "location": "string or null"
}}
 
Customer message: "{user_message}"
"""
    raw = call_gemini(prompt)
 
    # Gemini sometimes wraps JSON in ```json ... ``` even when told not to
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
 
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: if parsing fails, return an empty intent rather than crashing
        return {"category": None, "budget_max": None, "date_requested": None, "location": None}
