"""Memory Agent: Persistent cross-meeting memory & historical decision retriever."""
from typing import List, Dict, Any, Optional
from meetflow.database import operations

class MemoryAgent:
    """Agent responsible for managing persistent organizational memory."""

    def get_historical_decisions(self, exclude_meeting_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all active historical decisions from persistent memory,
        optionally excluding the current meeting.
        """
        all_decisions = operations.list_decisions()
        if exclude_meeting_id:
            return [d for d in all_decisions if d.get("meeting_id") != exclude_meeting_id and d.get("status") == "Active"]
        return [d for d in all_decisions if d.get("status") == "Active"]

    def record_decisions(self, meeting_id: str, decisions: List[Dict[str, Any]], meeting_title: str):
        """Persist new decisions to long-term memory."""
        for dec in decisions:
            operations.add_decision(
                meeting_id=meeting_id,
                decision_text=dec.get("decision_text", ""),
                category=dec.get("category", "General"),
                status="Active",
                source_meeting_title=meeting_title
            )

    def mark_decision_superseded(self, decision_id: str):
        """Update historical decision status when a confirmed update supersedes it."""
        operations.update_decision_status(decision_id, "Superseded")
