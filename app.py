"""
Image Analyzer Bot - Main Application

A Flask web application that uses Google's Gemini AI to analyze images
based on user prompts.
"""
import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

from config import get_config
from utils import (
    allowed_file,
    save_uploaded_file,
    cleanup_temp_file,
    analyze_image_with_gemini
)


def create_app(config_class=None):
    """
    Application factory function.
    
    Args:
        config_class: Configuration class to use (default: auto-detect)
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Validate API key
    if not app.config['GEMINI_API_KEY']:
        raise ValueError(
            "GEMINI_API_KEY not set. Please set it in your .env file or environment variables."
        )
    
    # Configure Google Generative AI
    genai.configure(api_key=app.config['GEMINI_API_KEY'])
    
    # Initialize the model
    model = genai.GenerativeModel(
        model_name=app.config['MODEL_NAME'],
        generation_config=app.config['GENERATION_CONFIG'],
    )
    
    # Store model in app context
    app.model = model
    
    # Register routes
    register_routes(app)
    
    return app


def register_routes(app):
    """Register application routes."""
    
    @app.route('/')
    def index():
        """Render the main page."""
        return render_template('index.html')
    
    @app.route('/analyze', methods=['POST'])
    def analyze():
        """
        Analyze an uploaded image with the given prompt.
        
        Expects:
            - image: Image file (multipart/form-data)
            - prompt: Analysis prompt (form field)
        
        Returns:
            JSON response with analysis result or error
        """
        # Validate image upload
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        image = request.files['image']
        prompt = request.form.get('prompt', '').strip()
        
        # Validate prompt
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Validate file selection
        if image.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Validate file type
        if not allowed_file(image.filename, app.config['ALLOWED_EXTENSIONS']):
            return jsonify({
                "error": f"File type not allowed. Allowed types: {', '.join(app.config['ALLOWED_EXTENSIONS'])}"
            }), 400
        
        image_path = None
        try:
            # Save uploaded file
            image_path = save_uploaded_file(image, app.config['UPLOAD_FOLDER'])
            
            # Analyze image
            result = analyze_image_with_gemini(app.model, image_path, prompt)
            
            return jsonify({"result": result})
            
        except Exception as e:
            app.logger.error(f"Error processing request: {e}")
            return jsonify({"error": "An error occurred while processing your request"}), 500
            
        finally:
            # Cleanup temporary file
            if image_path:
                cleanup_temp_file(image_path)
    
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify({"status": "healthy"})
    
    @app.errorhandler(413)
    def file_too_large(e):
        """Handle file too large error."""
        return jsonify({"error": "File too large. Maximum size is 16MB"}), 413
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle internal server error."""
        return jsonify({"error": "Internal server error"}), 500


# Create application instance
app = create_app()


if __name__ == "__main__":
    print(f"Starting Image Analyzer Bot on port {app.config['PORT']}...")
    print(f"Debug mode: {app.config['DEBUG']}")
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
