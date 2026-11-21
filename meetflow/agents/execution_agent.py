"""Execution Agent: Governs human approvals, task execution tracking, and digests."""
from datetime import datetime, date
from typing import List, Dict, Any
from meetflow.database import operations

class ExecutionAgent:
    """Agent responsible for Human-in-the-Loop task approvals and execution workflows."""

    def approve_task(self, task_id: str) -> None:
        """Approve an individual task, promoting it to the Execution Tracker."""
        operations.update_action_item(
            item_id=task_id,
            approval_status="Approved",
            execution_status="In Progress"
        )

    def reject_task(self, task_id: str) -> None:
        """Reject an extracted task."""
        operations.update_action_item(
            item_id=task_id,
            approval_status="Rejected"
        )

    def update_task_progress(self, task_id: str, new_status: str) -> None:
        """Update task execution status (Not Started, In Progress, Completed)."""
        operations.update_action_item(
            item_id=task_id,
            execution_status=new_status
        )

    def generate_weekly_digest(self) -> Dict[str, Any]:
        """Generate high-level weekly executive execution digest."""
        all_meetings = operations.list_meetings()
        all_decisions = operations.list_decisions()
        all_tasks = operations.list_action_items()
        all_conflicts = operations.list_conflicts()

        approved_tasks = [t for t in all_tasks if t.get("approval_status") == "Approved"]
        completed_tasks = [t for t in all_tasks if t.get("execution_status") == "Completed"]
        pending_approvals = [t for t in all_tasks if t.get("approval_status") == "Pending"]
        
        # Check overdue tasks (compare against current date if parseable)
        today_str = date.today().strftime("%Y-%m-%d")
        
        return {
            "total_meetings": len(all_meetings),
            "total_decisions": len(all_decisions),
            "total_tasks_extracted": len(all_tasks),
            "approved_tasks_count": len(approved_tasks),
            "completed_tasks_count": len(completed_tasks),
            "pending_approvals_count": len(pending_approvals),
            "total_conflicts_flagged": len(all_conflicts),
            "unresolved_conflicts": len([c for c in all_conflicts if c.get("resolution_status") == "Unresolved"]),
            "recent_decisions": all_decisions[:5],
            "active_tasks": approved_tasks,
            "generated_at": datetime.now().strftime("%B %d, %Y - %H:%M:%S")
        }
