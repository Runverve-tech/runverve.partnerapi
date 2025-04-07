from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Check if file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_mime_type(filename):
    """Determine MIME type based on file extension"""
    if filename.lower().endswith('png'):
        return 'image/png'
    elif filename.lower().endswith(('jpg', 'jpeg')):
        return 'image/jpeg'
    elif filename.lower().endswith('gif'):
        return 'image/gif'
    return None