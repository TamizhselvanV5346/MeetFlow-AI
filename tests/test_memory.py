"""Unit tests for Persistent Meeting Memory across SQLite connections."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from meetflow.database import operations

def test_persistent_memory_storage():
    # Clear test database
    operations.reset_all_data()

    # Store meeting
    m_id = operations.create_meeting(
        title="Q4 Architecture Review",
        date="2026-11-20",
        participants="Sarah, Dave",
        raw_transcript="Discussion on database sharding and SQLite persistence.",
        summary="Architecture review focused on SQLite persistent storage.",
        discussion_points=["Database schemas", "WAL mode"],
        unresolved_questions=["Benchmark latency"],
        dependencies=["SQLite 3.35+"]
    )
    assert m_id is not None

    # Store decisions
    d_id = operations.add_decision(
        meeting_id=m_id,
        decision_text="Adopt SQLite with WAL mode for all persistent storage.",
        category="Architecture",
        source_meeting_title="Q4 Architecture Review"
    )
    assert d_id is not None

    # Store tasks
    t_id = operations.add_action_item(
        meeting_id=m_id,
        task_description="Implement SQLite connection pooling.",
        responsible_person="Dave",
        deadline="2026-11-25",
        priority="High",
        approval_status="Pending",
        source_meeting_title="Q4 Architecture Review"
    )
    assert t_id is not None

    # Retrieve and verify persistence
    meetings = operations.list_meetings()
    assert len(meetings) == 1
    assert meetings[0]["title"] == "Q4 Architecture Review"

    decisions = operations.list_decisions()
    assert len(decisions) == 1
    assert "SQLite with WAL" in decisions[0]["decision_text"]
    assert decisions[0]["status"] == "Active"

    tasks = operations.list_action_items()
    assert len(tasks) == 1
    assert tasks[0]["responsible_person"] == "Dave"
    assert tasks[0]["approval_status"] == "Pending"

    # Test status updates
    operations.update_action_item(t_id, approval_status="Approved", execution_status="In Progress")
    updated_tasks = operations.list_action_items(approval_status="Approved")
    assert len(updated_tasks) == 1
    assert updated_tasks[0]["execution_status"] == "In Progress"

if __name__ == "__main__":
    test_persistent_memory_storage()
    print("✅ All persistent memory tests passed successfully!")
