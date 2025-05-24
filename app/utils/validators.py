# app/utils/validators.py

import re

def is_valid_email(email):
    """Basic email validation."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_positive_int(value):
    """Check if value is a positive integer."""
    try:
        return int(value) > 0
    except (ValueError, TypeError):
        return False
