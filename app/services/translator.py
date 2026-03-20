import re
from app.services.hf_client import hf_client


async def translate_text(text: str, source_lang: str, target_lang: str) -> tuple[str, str]:
    """
    Translate text from source_lang to target_lang.
    Returns (translated_text, pronunciation).
    If source == target, returns original text with pronunciation only.
    """
    # Bonus: skip translation when same language, just get pronunciation
    if source_lang == target_lang:
        prompt = (
            f"Provide the pronunciation (romanized/phonetic in English letters) "
            f"for the following {source_lang} text.\n\n"
            f"Text: {text}\n\n"
            f"Respond ONLY in this exact format (no extra text):\n"
            f"Translation: {text}\n"
            f"Pronunciation: <romanized pronunciation>"
        )
    else:
        prompt = (
            f"Translate the following text from {source_lang} to {target_lang}. "
            f"Also provide the pronunciation of the translated text in English letters (romanized).\n\n"
            f"Text: {text}\n\n"
            f"Respond ONLY in this exact format (no extra text, no explanations):\n"
            f"Translation: <translated text in {target_lang}>\n"
            f"Pronunciation: <romanized/phonetic pronunciation of the translation>"
        )

    raw = await hf_client.query(prompt)
    if not raw:
        raise ValueError("Translation returned an empty result.")

    return _parse_translation_response(raw, text)


def _parse_translation_response(raw: str, fallback_text: str) -> tuple[str, str]:
    """Parse 'Translation: ...\nPronunciation: ...' format from model output."""
    translation = ""
    pronunciation = ""

    for line in raw.splitlines():
        line = line.strip()
        low = line.lower()
        if low.startswith("translation:"):
            translation = line[len("translation:"):].strip()
        elif low.startswith("pronunciation:"):
            pronunciation = line[len("pronunciation:"):].strip()

    # Fallbacks if model didn't follow format
    if not translation:
        # Use the full response as translation if parsing fails
        translation = raw.strip()
    if not pronunciation:
        pronunciation = ""

    return translation, pronunciation