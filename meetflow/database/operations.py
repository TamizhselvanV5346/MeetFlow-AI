"""Database CRUD operations for persistent meeting intelligence."""
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from meetflow.database.connection import get_connection
from meetflow.database.models import init_db

# Initialize database tables on import
init_db()

# ----------------- Meetings -----------------
def create_meeting(
    title: str,
    date: str,
    participants: str,
    raw_transcript: str,
    summary: str = "",
    discussion_points: List[str] = None,
    unresolved_questions: List[str] = None,
    dependencies: List[str] = None,
    meeting_id: Optional[str] = None
) -> str:
    meeting_id = meeting_id or str(uuid.uuid4())
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO meetings (
                    id, title, date, participants, raw_transcript,
                    summary, discussion_points, unresolved_questions, dependencies
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    meeting_id,
                    title,
                    date,
                    participants,
                    raw_transcript,
                    summary,
                    json.dumps(discussion_points or []),
                    json.dumps(unresolved_questions or []),
                    json.dumps(dependencies or [])
                )
            )
        return meeting_id
    finally:
        conn.close()

def get_meeting(meeting_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM meetings WHERE id = ?", (meeting_id,))
        row = cur.fetchone()
        if not row:
            return None
        res = dict(row)
        res["discussion_points"] = json.loads(res["discussion_points"] or "[]")
        res["unresolved_questions"] = json.loads(res["unresolved_questions"] or "[]")
        res["dependencies"] = json.loads(res["dependencies"] or "[]")
        return res
    finally:
        conn.close()

def list_meetings() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM meetings ORDER BY date DESC, created_at DESC")
        rows = cur.fetchall()
        result = []
        for r in rows:
            item = dict(r)
            item["discussion_points"] = json.loads(item["discussion_points"] or "[]")
            item["unresolved_questions"] = json.loads(item["unresolved_questions"] or "[]")
            item["dependencies"] = json.loads(item["dependencies"] or "[]")
            result.append(item)
        return result
    finally:
        conn.close()

# ----------------- Decisions -----------------
def add_decision(
    meeting_id: str,
    decision_text: str,
    category: str = "General",
    status: str = "Active",
    timestamp: Optional[str] = None,
    source_meeting_title: str = "",
    decision_id: Optional[str] = None
) -> str:
    decision_id = decision_id or str(uuid.uuid4())
    ts = timestamp or datetime.now().isoformat()
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO decisions (id, meeting_id, decision_text, category, status, timestamp, source_meeting_title)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (decision_id, meeting_id, decision_text, category, status, ts, source_meeting_title)
            )
        return decision_id
    finally:
        conn.close()

def list_decisions(meeting_id: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        if meeting_id:
            cur.execute("SELECT * FROM decisions WHERE meeting_id = ? ORDER BY created_at DESC", (meeting_id,))
        else:
            cur.execute("SELECT * FROM decisions ORDER BY created_at DESC")
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()

def update_decision_status(decision_id: str, new_status: str):
    conn = get_connection()
    try:
        with conn:
            conn.execute("UPDATE decisions SET status = ? WHERE id = ?", (new_status, decision_id))
    finally:
        conn.close()

# ----------------- Action Items -----------------
def add_action_item(
    meeting_id: str,
    task_description: str,
    responsible_person: str = "Unassigned",
    deadline: str = "Unknown",
    priority: str = "Medium",
    approval_status: str = "Pending",
    source_meeting_title: str = "",
    item_id: Optional[str] = None
) -> str:
    item_id = item_id or str(uuid.uuid4())
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO action_items (
                    id, meeting_id, task_description, responsible_person,
                    deadline, priority, approval_status, execution_status, source_meeting_title
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'Not Started', ?)
                """,
                (item_id, meeting_id, task_description, responsible_person, deadline, priority, approval_status, source_meeting_title)
            )
        return item_id
    finally:
        conn.close()

def update_action_item(
    item_id: str,
    task_description: Optional[str] = None,
    responsible_person: Optional[str] = None,
    deadline: Optional[str] = None,
    priority: Optional[str] = None,
    approval_status: Optional[str] = None,
    execution_status: Optional[str] = None
):
    conn = get_connection()
    try:
        updates = []
        params = []
        if task_description is not None:
            updates.append("task_description = ?")
            params.append(task_description)
        if responsible_person is not None:
            updates.append("responsible_person = ?")
            params.append(responsible_person)
        if deadline is not None:
            updates.append("deadline = ?")
            params.append(deadline)
        if priority is not None:
            updates.append("priority = ?")
            params.append(priority)
        if approval_status is not None:
            updates.append("approval_status = ?")
            params.append(approval_status)
            if approval_status == "Approved":
                updates.append("approved_at = ?")
                params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if execution_status is not None:
            updates.append("execution_status = ?")
            params.append(execution_status)
            if execution_status == "Completed":
                updates.append("completed_at = ?")
                params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if not updates:
            return

        params.append(item_id)
        sql = f"UPDATE action_items SET {', '.join(updates)} WHERE id = ?"
        with conn:
            conn.execute(sql, tuple(params))
    finally:
        conn.close()

def list_action_items(meeting_id: Optional[str] = None, approval_status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM action_items WHERE 1=1"
        params = []
        if meeting_id:
            query += " AND meeting_id = ?"
            params.append(meeting_id)
        if approval_status:
            query += " AND approval_status = ?"
            params.append(approval_status)
        query += " ORDER BY created_at DESC"
        cur.execute(query, tuple(params))
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()

# ----------------- Decision Conflicts -----------------
def add_conflict(
    current_meeting_id: str,
    historical_decision_text: str,
    new_decision_text: str,
    conflict_type: str,
    explanation: str = "",
    recommended_action: str = "",
    historical_decision_id: Optional[str] = None,
    conflict_id: Optional[str] = None
) -> str:
    conflict_id = conflict_id or str(uuid.uuid4())
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO decision_conflicts (
                    id, current_meeting_id, historical_decision_id, historical_decision_text,
                    new_decision_text, conflict_type, explanation, recommended_action, resolution_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Unresolved')
                """,
                (
                    conflict_id,
                    current_meeting_id,
                    historical_decision_id,
                    historical_decision_text,
                    new_decision_text,
                    conflict_type,
                    explanation,
                    recommended_action
                )
            )
        return conflict_id
    finally:
        conn.close()

def list_conflicts(meeting_id: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        if meeting_id:
            cur.execute("SELECT * FROM decision_conflicts WHERE current_meeting_id = ? ORDER BY created_at DESC", (meeting_id,))
        else:
            cur.execute("SELECT * FROM decision_conflicts ORDER BY created_at DESC")
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()

def update_conflict_status(conflict_id: str, resolution_status: str):
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "UPDATE decision_conflicts SET resolution_status = ?, resolved_at = ? WHERE id = ?",
                (resolution_status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), conflict_id)
            )
    finally:
        conn.close()

def reset_all_data():
    """Clear all data for clean testing/demonstration."""
    conn = get_connection()
    try:
        with conn:
            conn.execute("DELETE FROM decision_conflicts")
            conn.execute("DELETE FROM action_items")
            conn.execute("DELETE FROM decisions")
            conn.execute("DELETE FROM meetings")
    finally:
        conn.close()
