from app.services.hf_client import hf_client


async def convert_tone(text: str, tone: str, language: str = "English") -> tuple[str, str]:
    """
    Convert tone of text while strictly preserving the given language.
    Returns (tone_converted_text, pronunciation).
    """
    prompt = (
        f"Rewrite the following text in a {tone} tone while keeping the language strictly as {language}. "
        f"Do NOT translate to another language. Do NOT change the language. "
        f"Only adjust the tone to be more {tone}. "
        f"Also provide the pronunciation of the rewritten text in English letters (romanized).\n\n"
        f"Text: {text}\n\n"
        f"Respond ONLY in this exact format (no extra text, no explanations):\n"
        f"Rewritten: <rewritten text in {language}>\n"
        f"Pronunciation: <romanized/phonetic pronunciation>"
    )

    raw = await hf_client.query(prompt)
    if not raw:
        raise ValueError("Tone conversion returned an empty result.")

    return _parse_tone_response(raw, text)


def _parse_tone_response(raw: str, fallback_text: str) -> tuple[str, str]:
    """Parse 'Rewritten: ...\nPronunciation: ...' format."""
    rewritten = ""
    pronunciation = ""

    for line in raw.splitlines():
        line = line.strip()
        low = line.lower()
        if low.startswith("rewritten:"):
            rewritten = line[len("rewritten:"):].strip()
        elif low.startswith("pronunciation:"):
            pronunciation = line[len("pronunciation:"):].strip()

    if not rewritten:
        rewritten = raw.strip()
    if not pronunciation:
        pronunciation = ""

    return rewritten, pronunciation