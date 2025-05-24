# app/utils/helpers.py

def format_date(dt, fmt="%Y-%m-%d"):
    """Format datetime object to string."""
    return dt.strftime(fmt)

def slugify(text):
    """Create a URL-friendly slug from text."""
    return text.lower().replace(' ', '-')
