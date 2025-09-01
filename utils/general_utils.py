from datetime import datetime


def make_version() -> str:
    """Generate a version string based on the current date."""
    return str(datetime.now().strftime("%Y%m%d_%H%M%S"))