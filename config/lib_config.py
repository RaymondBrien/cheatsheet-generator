from pathlib import Path

CHEATSHEET_DIR = Path("outputs") / "cheatsheets"
TOPIC_DIR: Path = Path("topics")  # Directory where topic files are stored

APP_NAME = 'templating_app'
DEFAULT_DIR = Path(__file__).parent
TEMPLATE_DIR = DEFAULT_DIR / 'templates'