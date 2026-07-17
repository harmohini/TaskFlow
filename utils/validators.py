import re


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password):
    """Validate password (min 6 chars)."""
    return len(password) >= 6


def validate_required(value):
    """Check if a required field has a value."""
    return bool(value and str(value).strip())


def validate_date(date_string):
    """Validate date format (YYYY-MM-DD)."""
    if not date_string:
        return True  # Optional date
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_string))