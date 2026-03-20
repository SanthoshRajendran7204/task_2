import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")
    # HF Router — OpenAI-compatible endpoint (correct URL, no provider suffix needed)
    HF_MODEL_URL: str = "https://router.huggingface.co/v1/chat/completions"
    # Llama 3.1 8B — free tier, widely available across providers
    HF_MODEL_ID: str = "meta-llama/Llama-3.1-8B-Instruct"

    SUPPORTED_LANGUAGES = {
        "English": "English",
        "Tamil": "Tamil",
        "Malayalam": "Malayalam",
        "Kannada": "Kannada",
        "Telugu": "Telugu",
        "Hindi": "Hindi",
    }

settings = Settings()
