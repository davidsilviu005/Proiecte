# ai/summarizer.py

import os

try:
    import openai  # pip install openai
except ImportError:
    openai = None


def summarize_text(text: str, max_sentences: int = 3) -> str:
    """
    Summarize a piece of text using an AI model.
    You MUST set the environment variable OPENAI_API_KEY before running.
    """
    if openai is None:
        return "[Error] openai package not installed. Run: pip install openai"

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[Error] OPENAI_API_KEY not set in environment."

    openai.api_key = api_key

    # This is approximate; check the latest OpenAI docs for exact syntax.
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or another model you have access to
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that summarizes student notes. "
                        f"Limit the summary to about {max_sentences} sentences."
                    ),
                },
                {"role": "user", "content": text},
            ],
            temperature=0.3,
        )
        summary = response["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        return f"[Error while calling AI: {e}]"
