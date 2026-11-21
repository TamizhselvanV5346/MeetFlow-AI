"""Conflict Agent: Evaluates newly proposed decisions against organizational memory."""
from typing import List, Dict, Any, Tuple
from meetflow.ai.extraction import detect_decision_conflicts
from meetflow.ai.schemas import ConflictDetectionResult
from meetflow.database import operations

class ConflictAgent:
    """Agent responsible for detecting contradictions, modified deadlines, and reversed decisions."""

    def analyze_conflicts(
        self,
        current_meeting_id: str,
        current_title: str,
        current_date: str,
        new_decisions: List[Dict[str, Any]],
        historical_decisions: List[Dict[str, Any]]
    ) -> Tuple[ConflictDetectionResult, str]:
        """
        Detect conflicts between new decisions and historical memory, and persist them.
        """
        detection_result, mode = detect_decision_conflicts(
            current_title=current_title,
            current_date=current_date,
            new_decisions=new_decisions,
            historical_decisions=historical_decisions
        )

        # Persist detected conflicts to database
        for item in detection_result.conflicts:
            operations.add_conflict(
                current_meeting_id=current_meeting_id,
                historical_decision_id=item.historical_decision_id,
                historical_decision_text=item.historical_decision_text,
                new_decision_text=item.new_decision_text,
                conflict_type=item.conflict_type,
                explanation=item.explanation,
                recommended_action=item.recommended_action
            )

        return detection_result, mode
