"""Database connection management for SQLite."""
import sqlite3
from pathlib import Path
from meetflow.config import DB_PATH

def get_connection() -> sqlite3.Connection:
    """Return a configured SQLite connection with row factory."""
    db_file = Path(DB_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_file), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys and WAL mode for reliability
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn
