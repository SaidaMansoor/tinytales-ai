# config.py
from pathlib import Path

# Application settings
APP_NAME = "AI Kids Story Generator"
APP_VERSION = "1.0.0"

# Directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, EXPORTS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Story generation settings
DEFAULT_STORY_LENGTH = 6
MAX_STORY_LENGTH = 10
MIN_STORY_LENGTH = 3

# Available options
GENRES = [
    "Adventure",
    "Fantasy", 
    "Educational",
    "Friendship",
    "Animal Stories",
    "Mystery",
    "Science Fiction"
]

GENDERS = [
    "Boy",
    "Girl", 
    "Non-binary",
    "Animal Character",
    "Mixed Group"
]

AGE_GROUPS = [
    "3-5 years",
    "5-7 years", 
    "7-9 years"
]

STORY_LENGTHS = [
    "5 pages",
    "6 pages",
    "7 pages", 
    "8 pages"
]

# Gemini AI settings
GEMINI_MODEL = "gemini-2.0-flash-exp"
MAX_TOKENS = 1500
TEMPERATURE = 0.8
TOP_P = 0.95
TOP_K = 40

# File settings
STORIES_FILENAME = "stories.json"
BACKUP_FILENAME = "stories_backup.json"