"""Task Service: Human approvals, execution status, metrics, and digest calculations."""
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from meetflow.database import operations
from meetflow.agents.execution_agent import ExecutionAgent

execution_agent = ExecutionAgent()

def get_pending_tasks(meeting_id: Optional[str] = None) -> List[Dict[str, Any]]:
    return operations.list_action_items(meeting_id=meeting_id, approval_status="Pending")

def get_approved_tasks(meeting_id: Optional[str] = None) -> List[Dict[str, Any]]:
    return operations.list_action_items(meeting_id=meeting_id, approval_status="Approved")

def approve_task(task_id: str):
    execution_agent.approve_task(task_id)

def reject_task(task_id: str):
    execution_agent.reject_task(task_id)

def edit_task(
    task_id: str,
    task_description: str,
    responsible_person: str,
    deadline: str,
    priority: str
):
    operations.update_action_item(
        item_id=task_id,
        task_description=task_description,
        responsible_person=responsible_person,
        deadline=deadline,
        priority=priority
    )

def update_execution_status(task_id: str, new_status: str):
    execution_agent.update_task_progress(task_id, new_status)

def get_dashboard_metrics() -> Dict[str, Any]:
    """Calculate key execution metrics for the dashboard."""
    meetings = operations.list_meetings()
    decisions = operations.list_decisions()
    tasks = operations.list_action_items()
    conflicts = operations.list_conflicts()

    approved = [t for t in tasks if t["approval_status"] == "Approved"]
    pending = [t for t in tasks if t["approval_status"] == "Pending"]
    rejected = [t for t in tasks if t["approval_status"] == "Rejected"]
    
    completed = [t for t in approved if t["execution_status"] == "Completed"]
    in_progress = [t for t in approved if t["execution_status"] == "In Progress"]
    not_started = [t for t in approved if t["execution_status"] == "Not Started"]

    # Basic deadline categorization
    today_str = date.today().strftime("%Y-%m-%d")
    overdue_count = 0
    due_today_count = 0
    upcoming_count = 0

    for t in approved:
        d_str = t.get("deadline", "").strip()
        if not d_str or d_str.lower() in ["unknown", "tbd", "none"]:
            continue
        try:
            # Try parsing ISO format YYYY-MM-DD
            d_obj = datetime.strptime(d_str, "%Y-%m-%d").date()
            today_obj = date.today()
            if t["execution_status"] != "Completed":
                if d_obj < today_obj:
                    overdue_count += 1
                elif d_obj == today_obj:
                    due_today_count += 1
                else:
                    upcoming_count += 1
        except Exception:
            # Non-ISO deadline format (e.g., 'December 10')
            pass

    return {
        "total_meetings": len(meetings),
        "total_decisions": len(decisions),
        "total_tasks": len(tasks),
        "pending_approvals": len(pending),
        "approved_tasks": len(approved),
        "rejected_tasks": len(rejected),
        "completed_tasks": len(completed),
        "in_progress_tasks": len(in_progress),
        "not_started_tasks": len(not_started),
        "total_conflicts": len(conflicts),
        "unresolved_conflicts": len([c for c in conflicts if c["resolution_status"] == "Unresolved"]),
        "overdue_tasks": overdue_count,
        "due_today_tasks": due_today_count,
        "upcoming_deadlines": upcoming_count
    }

def get_weekly_digest() -> Dict[str, Any]:
    return execution_agent.generate_weekly_digest()
