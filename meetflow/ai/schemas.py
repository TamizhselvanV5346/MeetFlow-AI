"""Pydantic validation schemas for MeetFlow AI."""
from typing import List, Optional
from pydantic import BaseModel, Field

class ActionItemExtraction(BaseModel):
    task_description: str = Field(description="Clear, actionable task description")
    responsible_person: str = Field(default="Unassigned", description="Person or role assigned. Set 'Unassigned' if missing")
    deadline: str = Field(default="Unknown", description="Target deadline or date. Set 'Unknown' if not mentioned")
    priority: str = Field(default="Medium", description="Priority level: Low, Medium, High, or Critical")

class DecisionExtraction(BaseModel):
    decision_text: str = Field(description="Clear statement of the decision made")
    category: str = Field(default="General", description="Category such as Product, Engineering, Marketing, Schedule, Budget")

class MeetingExtractionResult(BaseModel):
    summary: str = Field(description="Executive summary of the meeting")
    discussion_points: List[str] = Field(default_factory=list, description="Key discussion points")
    decisions: List[DecisionExtraction] = Field(default_factory=list, description="Decisions agreed upon in this meeting")
    action_items: List[ActionItemExtraction] = Field(default_factory=list, description="Action items with owners and deadlines")
    dependencies: List[str] = Field(default_factory=list, description="Identified technical or team dependencies")
    unresolved_questions: List[str] = Field(default_factory=list, description="Open or unresolved questions")

class DecisionConflictItem(BaseModel):
    historical_decision_id: Optional[str] = None
    historical_decision_text: str = Field(description="The previous decision that is affected")
    new_decision_text: str = Field(description="The newly proposed or contradictory decision")
    conflict_type: str = Field(
        description="Type: Deadline Modification, Responsibility Reassignment, Contradiction, Cancellation, Reversal, Potentially Conflicting Commitment"
    )
    explanation: str = Field(description="Detailed explanation of the contradiction or difference")
    recommended_action: str = Field(description="Recommended resolution action for human reviewers")

class ConflictDetectionResult(BaseModel):
    conflicts: List[DecisionConflictItem] = Field(default_factory=list)
