"""Memory Service: Persistent decision query and organizational memory service."""
from typing import List, Dict, Any
from meetflow.database import operations

def get_all_decisions(meeting_id: str = None) -> List[Dict[str, Any]]:
    """Retrieve decisions from persistent storage."""
    return operations.list_decisions(meeting_id=meeting_id)

def get_memory_timeline() -> List[Dict[str, Any]]:
    """Retrieve chronological timeline of organizational decisions and meetings."""
    meetings = operations.list_meetings()
    decisions = operations.list_decisions()
    
    # Map decisions to meetings
    meeting_map = {m["id"]: m for m in meetings}
    timeline = []
    for d in decisions:
        m = meeting_map.get(d["meeting_id"], {})
        timeline.append({
            "decision_id": d["id"],
            "decision_text": d["decision_text"],
            "category": d["category"],
            "status": d["status"],
            "meeting_title": m.get("title", d.get("source_meeting_title", "Unknown Meeting")),
            "meeting_date": m.get("date", "Unknown Date"),
            "timestamp": d["timestamp"]
        })
    return timeline
