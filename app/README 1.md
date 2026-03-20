# Language Translator API
### FastAPI + Hugging Face (flan-t5-large) + Vanilla JS Frontend

---

## Project Structure

```
translator_project/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   └── routes.py            # /translate, /tone, /translate-tone
│   ├── services/
│   │   ├── hf_client.py         # Hugging Face Inference API client
│   │   ├── translator.py        # Translation service
│   │   └── tone_converter.py    # Tone conversion service
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response models
│   └── core/
│       └── config.py            # Settings / env vars
├── frontend/
│   └── index.html               # Full UI (HTML + CSS + JS)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quick Start

### 1. Clone / enter the project directory
```bash
cd translator_project
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
# or
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your Hugging Face API key
```bash
cp .env.example .env
# Edit .env and replace the placeholder with your real token:
# HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
Get your free token at: https://huggingface.co/settings/tokens

### 5. Run the server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open the app
- **Frontend UI**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

---

## API Reference

### POST /api/translate
```json
// Request
{ "text": "Hello", "source_lang": "English", "target_lang": "Tamil" }

// Response
{ "translated_text": "வணக்கம்" }
```

### POST /api/tone
```json
// Request
{ "text": "hey wanna grab lunch?", "tone": "formal" }

// Response
{ "converted_text": "Would you like to have lunch together?" }
```

### POST /api/translate-tone
```json
// Request
{ "text": "Hello", "source_lang": "English", "target_lang": "Hindi", "tone": "casual" }

// Response
{ "output": "हेलो!" }
```

---

## Supported Languages
- English
- Tamil
- Malayalam
- Kannada
- Telugu
- Hindi

---

## Notes
- First request may take 20–30s if the HF model is cold-loading (503 is retried automatically)
- The app uses `google/flan-t5-large` via the HF Inference API (free tier available)
- Frontend is served at `/` by FastAPI itself — no separate web server needed
