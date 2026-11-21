"""MeetFlow AI Configuration Module."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_DB_PATH = str(DATA_DIR / "meetflow.db")
DB_PATH = os.getenv("MEETFLOW_DB_PATH", DEFAULT_DB_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

IS_LIVE_GEMINI = bool(GEMINI_API_KEY and len(GEMINI_API_KEY) > 10)
