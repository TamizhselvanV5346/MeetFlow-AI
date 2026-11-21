"""Conflict Service: Conflict resolution and audit management."""
from typing import List, Dict, Any
from meetflow.database import operations

def resolve_conflict(conflict_id: str, resolution_status: str, historical_decision_id: str = None):
    """
    Resolve a detected conflict:
    - Confirmed Update: New decision confirmed, historical decision updated/superseded.
    - Unresolved: Remains flagged for leadership review.
    - Rejected: New proposal rejected, historical decision stands.
    """
    operations.update_conflict_status(conflict_id, resolution_status)
    if resolution_status == "Confirmed Update" and historical_decision_id:
        operations.update_decision_status(historical_decision_id, "Superseded")
    elif resolution_status == "Rejected" and historical_decision_id:
        operations.update_decision_status(historical_decision_id, "Active")

def get_all_conflicts(meeting_id: str = None) -> List[Dict[str, Any]]:
    return operations.list_conflicts(meeting_id=meeting_id)
