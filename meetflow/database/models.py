"""SQLite schema definitions and migrations for MeetFlow AI."""
from meetflow.database.connection import get_connection

INIT_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS meetings (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    participants TEXT NOT NULL,
    raw_transcript TEXT NOT NULL,
    summary TEXT,
    discussion_points TEXT,
    unresolved_questions TEXT,
    dependencies TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    meeting_id TEXT NOT NULL,
    decision_text TEXT NOT NULL,
    category TEXT DEFAULT 'General',
    status TEXT DEFAULT 'Active', -- Active, Superseded, Conflicted, Revoked
    timestamp TEXT NOT NULL,
    source_meeting_title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS action_items (
    id TEXT PRIMARY KEY,
    meeting_id TEXT NOT NULL,
    task_description TEXT NOT NULL,
    responsible_person TEXT NOT NULL DEFAULT 'Unassigned',
    deadline TEXT NOT NULL DEFAULT 'Unknown',
    priority TEXT NOT NULL DEFAULT 'Medium', -- Low, Medium, High, Critical
    approval_status TEXT NOT NULL DEFAULT 'Pending', -- Pending, Approved, Rejected
    execution_status TEXT NOT NULL DEFAULT 'Not Started', -- Not Started, In Progress, Completed
    approved_at TEXT,
    completed_at TEXT,
    source_meeting_title TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS decision_conflicts (
    id TEXT PRIMARY KEY,
    current_meeting_id TEXT NOT NULL,
    historical_decision_id TEXT,
    historical_decision_text TEXT NOT NULL,
    new_decision_text TEXT NOT NULL,
    conflict_type TEXT NOT NULL, -- Deadline Modification, Responsibility Reassignment, Contradiction, Cancellation, Reversal
    explanation TEXT,
    recommended_action TEXT,
    resolution_status TEXT NOT NULL DEFAULT 'Unresolved', -- Unresolved, Confirmed Update, Rejected
    resolved_at TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(current_meeting_id) REFERENCES meetings(id) ON DELETE CASCADE,
    FOREIGN KEY(historical_decision_id) REFERENCES decisions(id) ON DELETE SET NULL
);
"""

def init_db():
    """Initialize SQLite tables if they do not exist."""
    conn = get_connection()
    try:
        with conn:
            conn.executescript(INIT_SCHEMA_SQL)
    finally:
        conn.close()
