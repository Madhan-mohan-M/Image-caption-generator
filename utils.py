"""
Utility functions for the Image Analyzer Bot.
"""
import os
import mimetypes
from werkzeug.utils import secure_filename
import google.generativeai as genai


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename: The name of the uploaded file
        allowed_extensions: Set of allowed file extensions
    
    Returns:
        True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_mime_type(filename: str) -> str:
    """
    Get the MIME type of a file based on its extension.
    
    Args:
        filename: The name of the file
    
    Returns:
        MIME type string, defaults to 'application/octet-stream'
    """
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or 'application/octet-stream'


def save_uploaded_file(file, upload_folder: str) -> str:
    """
    Save an uploaded file to the specified folder.
    
    Args:
        file: The uploaded file object
        upload_folder: Directory to save the file
    
    Returns:
        Full path to the saved file
    """
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filepath


def cleanup_temp_file(filepath: str) -> bool:
    """
    Remove a temporary file after processing.
    
    Args:
        filepath: Path to the file to remove
    
    Returns:
        True if file was removed, False otherwise
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except OSError as e:
        print(f"Error removing temp file {filepath}: {e}")
    return False


def upload_to_gemini(path: str, mime_type: str = None):
    """
    Upload a file to Google Gemini.
    
    Args:
        path: Path to the file to upload
        mime_type: MIME type of the file (auto-detected if None)
    
    Returns:
        Uploaded file object from Gemini
    """
    if mime_type is None:
        mime_type = get_mime_type(path)
    
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


def analyze_image_with_gemini(model, image_path: str, prompt: str) -> str:
    """
    Analyze an image using Google Gemini model.
    
    Args:
        model: The Gemini model instance
        image_path: Path to the image file
        prompt: User prompt for analysis
    
    Returns:
        Analysis result text
    """
    try:
        # Get the correct MIME type
        mime_type = get_mime_type(image_path)
        
        # Upload image to Gemini
        uploaded_file = upload_to_gemini(image_path, mime_type=mime_type)
        
        # Start chat session and get response
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [uploaded_file, prompt],
                }
            ]
        )
        
        response = chat_session.send_message(prompt)
        
        if response:
            return response.text
        else:
            return "Error occurred while analyzing the image"
            
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return f"Error analyzing image: {str(e)}"
