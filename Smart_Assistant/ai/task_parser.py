# ai/task_parser.py
import os
import json
import openai


def parse_task_nl(text: str) -> dict:
    """
    Parse a natural language task description into structured fields.
    Returns dict with keys like: title, due_date (YYYY-MM-DD), description.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY not set"}

    openai.api_key = api_key

    prompt = f"""
    You will receive a student's natural language description of a task.
    Extract:
    - title (short)
    - due_date in ISO format YYYY-MM-DD if a date is mentioned, else empty
    - description (optional extra details)

    Respond ONLY as valid JSON with keys: title, due_date, description.

    Text: "{text}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw = response["choices"][0]["message"]["content"]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"title": text[:50], "due_date": "", "description": text}
    return data
