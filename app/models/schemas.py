from pydantic import BaseModel
from typing import Literal, Optional


class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str


class TranslateResponse(BaseModel):
    translated_text: str
    pronunciation: str


class ToneRequest(BaseModel):
    text: str
    tone: Literal["formal", "casual"]
    language: str = "English"   # language to preserve during tone conversion


class ToneResponse(BaseModel):
    converted_text: str
    pronunciation: str


class TranslateToneRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    tone: Literal["formal", "casual"]


class TranslateToneResponse(BaseModel):
    output: str
    pronunciation: str