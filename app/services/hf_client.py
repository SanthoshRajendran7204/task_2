import httpx
import asyncio
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class HuggingFaceClient:
    def __init__(self):
        self.url = settings.HF_MODEL_URL
        self.model = settings.HF_MODEL_ID
        self.headers = {
            "Authorization": f"Bearer {settings.HF_API_KEY}",
            "Content-Type": "application/json",
        }
        token = settings.HF_API_KEY
        if not token or len(token) < 10:
            logger.error("⚠️  HF_API_KEY is missing or too short! Check your .env file.")
        masked = f"{token[:8]}...{token[-4:]}" if len(token) > 12 else "(empty or missing!)"
        logger.info(f"HF Client ready | model: {self.model} | token: {masked}")

    async def query(self, prompt: str, retries: int = 3, wait: int = 20) -> str:
        """
        Call HF Inference via OpenAI-compatible /v1/chat/completions endpoint.
        """
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "max_tokens": 512,
            "temperature": 0.3,
        }

        logger.info(f"Prompt preview: {prompt[:100]!r}")

        async with httpx.AsyncClient(timeout=60.0) as client:
            for attempt in range(retries):
                logger.info(f"Attempt {attempt + 1}/{retries} → {self.url}")

                response = await client.post(
                    self.url,
                    headers=self.headers,
                    json=payload,
                )

                logger.info(f"Status: {response.status_code} | Body: {response.text[:300]}")

                if response.status_code == 200:
                    data = response.json()
                    try:
                        result = data["choices"][0]["message"]["content"].strip()
                        logger.info(f"Result: {result[:120]!r}")
                        return result
                    except (KeyError, IndexError) as e:
                        raise ValueError(f"Unexpected response structure: {data}") from e

                elif response.status_code == 503:
                    logger.warning(f"503 — model loading, retrying in {wait}s...")
                    if attempt < retries - 1:
                        await asyncio.sleep(wait)
                        continue
                    raise RuntimeError("Model is still loading. Please try again in a moment.")

                elif response.status_code == 401:
                    raise RuntimeError(
                        "Invalid Hugging Face API token. Check your .env file."
                    )

                elif response.status_code == 429:
                    raise RuntimeError(
                        "HF rate limit hit. Please wait a moment and try again."
                    )

                else:
                    raise RuntimeError(
                        f"HF API error {response.status_code}: {response.text}"
                    )

        raise RuntimeError("Failed to get a response from Hugging Face after all retries.")


hf_client = HuggingFaceClient()

