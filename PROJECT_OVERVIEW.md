# Project Overview: Image Analyzer Bot

## Summary
A web application that analyzes images using Google's Gemini AI. Users upload an image and ask questions about it — the AI provides detailed analysis.

## Tech Stack
| Layer | Technology |
|-------|------------|
| Backend | Flask (Python) |
| AI | Google Gemini 2.0 Flash |
| Frontend | HTML/CSS/JavaScript |

## Architecture
```
User → Web UI → Flask API → Google Gemini AI → Response
```

## Key Files
| File | Purpose |
|------|---------|
| `app.py` | Flask application with routes and factory pattern |
| `config.py` | Environment-based configuration (dev/prod) |
| `utils.py` | File handling, MIME detection, Gemini API wrapper |
| `templates/index.html` | Modern UI with drag-drop, preview, loading states |

## API Endpoints
- `GET /` — Main interface
- `POST /analyze` — Image analysis (multipart form: image + prompt)
- `GET /health` — Health check

## Security
- API key stored in `.env` (not committed)
- File type validation
- Secure filename handling
- Temp file cleanup after processing

## Running
```bash
pip install -r requirements.txt
cp .env.example .env  # Add your GEMINI_API_KEY
python app.py         # http://localhost:5656
```
