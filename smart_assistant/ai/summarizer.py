# ai/summarizer.py
#
# Offline summarizer using Hugging Face transformers.
# No API key, no billing. After the first model download, it works offline.

from typing import Optional

try:
    from transformers import pipeline
except ImportError:
    pipeline = None

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"  # lightweight summarization model

_summarizer = None
_load_error: Optional[str] = None


def _load_summarizer():
    """
    Lazy-load the summarization pipeline.
    Called automatically the first time summarize_text() is used.
    """
    global _summarizer, _load_error

    if pipeline is None:
        _load_error = (
            "The 'transformers' package is not installed. "
            "Run: pip install transformers torch"
        )
        return

    if _summarizer is not None:
        return  # already loaded

    try:
        _summarizer = pipeline("summarization", model=MODEL_NAME)
    except Exception as e:
        _load_error = f"Error loading summarization model: {e}"
        _summarizer = None


def summarize_text(text: str, max_sentences: int = 3) -> str:
    """
    Summarize a piece of text locally using a transformer model.

    Args:
        text: original note content
        max_sentences: approximate number of sentences to aim for

    Returns:
        Summary string or an error message (starting with [Error]).
    """
    global _summarizer, _load_error

    if not text or len(text.strip()) == 0:
        return "[Error] No text to summarize."

    # Load model on first call
    if _summarizer is None and _load_error is None:
        _load_summarizer()

    if _load_error is not None:
        return f"[Error] { _load_error }"

    # For very short text, just return it
    cleaned = text.strip()
    if len(cleaned) < 80:
        return cleaned

    # Heuristic: tokens ~ words, so tune length based on desired sentences
    max_length = max(30, 40 * max_sentences)
    min_length = max(10, 15 * max_sentences)

    # Some models have a max token limit; if the note is huge, truncate it
    # to keep things fast and avoid errors.
    if len(cleaned) > 3000:
        cleaned = cleaned[:3000]

    try:
        result = _summarizer(
            cleaned,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )
        summary = result[0]["summary_text"].strip()
        return summary
    except Exception as e:
        return f"[Error] Could not summarize text: {e}"
