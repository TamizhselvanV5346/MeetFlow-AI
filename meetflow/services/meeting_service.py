"""Meeting Service: End-to-end ingestion and orchestration pipeline."""
from typing import Dict, Any, List
from meetflow.agents.meeting_agent import MeetingAgent
from meetflow.agents.memory_agent import MemoryAgent
from meetflow.agents.conflict_agent import ConflictAgent
from meetflow.database import operations

meeting_agent = MeetingAgent()
memory_agent = MemoryAgent()
conflict_agent = ConflictAgent()

def ingest_and_process_meeting(
    title: str,
    date: str,
    participants: str,
    transcript: str
) -> Dict[str, Any]:
    """
    Executes the full agentic meeting intelligence pipeline:
    1. Retrieve historical decisions from Persistent Memory.
    2. Process transcript with MeetingAgent (Gemini / validated extraction).
    3. Persist meeting record and extracted action items (with 'Pending' approval status).
    4. Persist newly extracted decisions into Memory.
    5. Detect decision conflicts against historical memory with ConflictAgent.
    """
    # Step 1: Retrieve existing historical decisions prior to saving this meeting
    historical_decisions = memory_agent.get_historical_decisions()

    # Step 2: AI extraction
    extraction, mode = meeting_agent.process_transcript(
        title=title,
        date=date,
        participants=participants,
        transcript=transcript
    )

    # Step 3: Persist meeting
    meeting_id = operations.create_meeting(
        title=title,
        date=date,
        participants=participants,
        raw_transcript=transcript,
        summary=extraction.summary,
        discussion_points=extraction.discussion_points,
        unresolved_questions=extraction.unresolved_questions,
        dependencies=extraction.dependencies
    )

    # Step 4: Persist action items in Pending state for Human Approval
    created_tasks = []
    for item in extraction.action_items:
        task_id = operations.add_action_item(
            meeting_id=meeting_id,
            task_description=item.task_description,
            responsible_person=item.responsible_person or "Unassigned",
            deadline=item.deadline or "Unknown",
            priority=item.priority or "Medium",
            approval_status="Pending",
            source_meeting_title=title
        )
        created_tasks.append(task_id)

    # Step 5: Convert decisions to dict and persist into persistent memory
    new_decisions_dict = [d.model_dump() for d in extraction.decisions]
    memory_agent.record_decisions(
        meeting_id=meeting_id,
        decisions=new_decisions_dict,
        meeting_title=title
    )

    # Step 6: Decision Conflict Detection
    conflict_result, conflict_mode = conflict_agent.analyze_conflicts(
        current_meeting_id=meeting_id,
        current_title=title,
        current_date=date,
        new_decisions=new_decisions_dict,
        historical_decisions=historical_decisions
    )

    return {
        "meeting_id": meeting_id,
        "extraction": extraction,
        "engine_mode": mode,
        "conflict_result": conflict_result,
        "conflict_mode": conflict_mode,
        "historical_decisions_evaluated": len(historical_decisions),
        "tasks_created_count": len(created_tasks)
    }
