# Image Analyzer Bot

A Flask web application that uses Google's Gemini AI to analyze images based on user prompts.

## Features

- Upload any image and ask questions about it
- Powered by Google Gemini 2.0 Flash model
- Modern, responsive UI with drag-and-drop support
- Image preview before analysis
- Real-time loading indicators

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Image-caption-generator
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### 5. Run the application

```bash
python app.py
```

The application will be available at `http://localhost:5656`

## Project Structure

```
Image-caption-generator/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── templates/
│   └── index.html      # Frontend UI
└── temp/               # Temporary file storage (auto-created)
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/analyze` | POST | Analyze an uploaded image |
| `/health` | GET | Health check endpoint |

## Configuration Options

All configuration can be set via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | (required) | Your Google Gemini API key |
| `FLASK_ENV` | development | Environment mode |
| `FLASK_DEBUG` | True | Enable debug mode |
| `PORT` | 5656 | Server port |
| `MODEL_NAME` | gemini-2.0-flash | Gemini model to use |
| `MODEL_TEMPERATURE` | 1 | Model temperature (0-1) |
| `MODEL_MAX_TOKENS` | 8192 | Maximum output tokens |

## Usage

1. Open the application in your browser
2. Enter a prompt describing what you want to know about the image
3. Upload an image (drag-and-drop or click to browse)
4. Click "Analyze Image"
5. View the AI-generated analysis

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- WebP
- BMP

Maximum file size: 16MB

## License

MIT License
