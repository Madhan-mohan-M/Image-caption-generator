"""
Configuration settings for the Image Analyzer Bot.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    PORT = int(os.getenv('PORT', 5656))
    
    # Google Gemini API settings
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Model configuration
    GENERATION_CONFIG = {
        "temperature": float(os.getenv('MODEL_TEMPERATURE', 1)),
        "top_p": float(os.getenv('MODEL_TOP_P', 0.95)),
        "top_k": int(os.getenv('MODEL_TOP_K', 64)),
        "max_output_tokens": int(os.getenv('MODEL_MAX_TOKENS', 8192)),
        "response_mime_type": "text/plain",
    }
    
    MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-2.0-flash')
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment."""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
