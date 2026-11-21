"""End-to-End tests for Cross-Meeting Decision Conflict Detection."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from meetflow.database import operations
from meetflow.services.meeting_service import ingest_and_process_meeting
from meetflow.services.conflict_service import resolve_conflict, get_all_conflicts

def test_two_meeting_conflict_detection_scenario():
    # 1. Reset database
    operations.reset_all_data()

    # 2. Ingest Meeting 1: Product Launch Planning
    m1_title = "Product Launch Planning"
    m1_date = "2026-12-01"
    m1_participants = "Manager, Developer, Marketing Lead"
    m1_transcript = """
    Manager: We are planning to launch our new product on December 10.
    Developer: I will complete the authentication module by December 5.
    Marketing Lead: I will prepare the promotional campaign before December 8.
    Manager: The development team must complete all testing before launch.
    """

    res1 = ingest_and_process_meeting(m1_title, m1_date, m1_participants, m1_transcript)
    assert res1["meeting_id"] is not None
    assert len(res1["conflict_result"].conflicts) == 0  # First meeting has no conflicts
    
    # Verify Meeting 1 decisions stored in persistent memory
    historical_decisions = operations.list_decisions()
    assert len(historical_decisions) >= 1
    dec10 = next(d for d in historical_decisions if "december 10" in d["decision_text"].lower())
    assert dec10 is not None

    # 3. Ingest Meeting 2: Product Launch Review (Postponing to Dec 15)
    m2_title = "Product Launch Review"
    m2_date = "2026-12-04"
    m2_participants = "Manager, Developer, Marketing Lead"
    m2_transcript = """
    Manager: Due to development delays, we are postponing the product launch to December 15.
    Developer: Authentication testing will require additional time.
    Marketing Lead: I will update the promotional campaign according to the new launch date.
    """

    res2 = ingest_and_process_meeting(m2_title, m2_date, m2_participants, m2_transcript)
    assert res2["meeting_id"] is not None
    
    # 4. CRITICAL VERIFICATION: Conflict detection
    conflicts = res2["conflict_result"].conflicts
    assert len(conflicts) >= 1, "Expected at least 1 decision conflict detected!"
    
    launch_conflict = next(c for c in conflicts if "launch" in c.new_decision_text.lower())
    assert launch_conflict is not None
    assert launch_conflict.conflict_type == "Deadline Modification"
    assert "december 10" in launch_conflict.historical_decision_text.lower()
    assert "december 15" in launch_conflict.new_decision_text.lower()
    
    # 5. Verify database conflict records
    db_conflicts = get_all_conflicts()
    assert len(db_conflicts) >= 1
    assert db_conflicts[0]["resolution_status"] == "Unresolved"

    # 6. Test resolving the conflict
    conflict_id = db_conflicts[0]["id"]
    resolve_conflict(conflict_id, "Confirmed Update", historical_decision_id=db_conflicts[0]["historical_decision_id"])
    
    updated_conflicts = get_all_conflicts()
    assert updated_conflicts[0]["resolution_status"] == "Confirmed Update"

    # Check that historical decision was superseded
    decisions_after = operations.list_decisions()
    old_dec = next(d for d in decisions_after if d["id"] == db_conflicts[0]["historical_decision_id"])
    assert old_dec["status"] == "Superseded"

if __name__ == "__main__":
    test_two_meeting_conflict_detection_scenario()
    print("✅ All cross-meeting conflict detection tests passed successfully!")
