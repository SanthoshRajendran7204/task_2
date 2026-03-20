from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    TranslateRequest, TranslateResponse,
    ToneRequest, ToneResponse,
    TranslateToneRequest, TranslateToneResponse,
)
from app.services.translator import translate_text
from app.services.tone_converter import convert_tone
from app.core.config import settings

router = APIRouter()


@router.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    _validate_languages(request.source_lang, request.target_lang)
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        translated, pronunciation = await translate_text(
            request.text, request.source_lang, request.target_lang
        )
        return TranslateResponse(translated_text=translated, pronunciation=pronunciation)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/tone", response_model=ToneResponse)
async def tone(request: ToneRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        converted, pronunciation = await convert_tone(
            request.text, request.tone, language=request.language
        )
        return ToneResponse(converted_text=converted, pronunciation=pronunciation)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/translate-tone", response_model=TranslateToneResponse)
async def translate_and_tone(request: TranslateToneRequest):
    _validate_languages(request.source_lang, request.target_lang)
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        # Step 1: Translate (or skip if same language)
        translated, _ = await translate_text(
            request.text, request.source_lang, request.target_lang
        )

        # Step 2: Apply tone IN the target language (not English!)
        final, pronunciation = await convert_tone(
            translated, request.tone, language=request.target_lang
        )

        return TranslateToneResponse(output=final, pronunciation=pronunciation)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=502, detail=str(e))


def _validate_languages(*langs: str):
    supported = set(settings.SUPPORTED_LANGUAGES.keys())
    for lang in langs:
        if lang not in supported:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: '{lang}'. Supported: {sorted(supported)}",
            )

