# utils/validators.py
import re

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """Validate password meets complexity requirements"""
    if not password or len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):  # At least one uppercase
        return False
    if not re.search(r'[a-z]', password):  # At least one lowercase
        return False
    if not re.search(r'[0-9]', password):  # At least one number
        return False
    if not re.search(r'[^A-Za-z0-9]', password):  # At least one special char
        return False
    return True

def validate_phone_number(phone):
    """Validate phone number format (10 digits)"""
    if not phone:
        return False
    return bool(re.match(r'^\d{10}$', phone))