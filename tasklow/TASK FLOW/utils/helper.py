from datetime import datetime, date


def format_date(value):
    """Format a date object to a readable string."""
    if isinstance(value, datetime):
        return value.strftime("%d %b, %Y")
    if isinstance(value, date):
        return value.strftime("%d %b, %Y")
    if isinstance(value, str):
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            return dt.strftime("%d %b, %Y")
        except ValueError:
            return value
    return value


def time_ago(value):
    """Return a human-readable time difference."""
    if not value:
        return ""

    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return value

    now = datetime.now()
    diff = now - value

    if diff.days > 365:
        years = diff.days // 365
        return f"{years}y ago"
    if diff.days > 30:
        months = diff.days // 30
        return f"{months}mo ago"
    if diff.days > 0:
        return f"{diff.days}d ago"
    if diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    if diff.seconds > 60:
        mins = diff.seconds // 60
        return f"{mins}m ago"
    return "just now"


def get_status_badge(status):
    """Return a Bootstrap badge class for a given status."""
    badges = {
        "Active": "bg-success",
        "On Hold": "bg-warning text-dark",
        "Completed": "bg-primary",
        "Cancelled": "bg-danger",
        "To Do": "bg-secondary",
        "In Progress": "bg-info text-dark",
        "Review": "bg-warning text-dark",
        "Low": "bg-success",
        "Medium": "bg-info text-dark",
        "High": "bg-warning text-dark",
        "Critical": "bg-danger"
    }
    return badges.get(status, "bg-secondary")


def truncate(text, length=50):
    """Truncate text to a given length."""
    if not text:
        return ""
    if len(text) <= length:
        return text
    return text[:length] + "..."