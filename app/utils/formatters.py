# app/utils/formatters.py

def format_currency(amount, symbol='$'):
    """Format number as currency string."""
    return f"{symbol}{amount:,.2f}"

def truncate_text(text, max_length=100):
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'
