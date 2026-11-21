"""Unit tests for Meeting Extraction and Pydantic validation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from meetflow.ai.extraction import extract_meeting_intelligence
from meetflow.ai.schemas import MeetingExtractionResult

def test_extraction_structure_meeting1():
    title = "Product Launch Planning"
    date = "2026-12-01"
    participants = "Manager, Developer, Marketing Lead"
    transcript = """
    Manager: We are planning to launch our new product on December 10.
    Developer: I will complete the authentication module by December 5.
    Marketing Lead: I will prepare the promotional campaign before December 8.
    Manager: The development team must complete all testing before launch.
    """
    
    result, mode = extract_meeting_intelligence(title, date, participants, transcript)
    
    assert isinstance(result, MeetingExtractionResult)
    assert len(result.decisions) >= 1
    assert any("december 10" in d.decision_text.lower() for d in result.decisions)
    
    assert len(result.action_items) >= 2
    # Verify action item fields
    auth_task = next((t for t in result.action_items if "authentication" in t.task_description.lower()), None)
    assert auth_task is not None
    assert auth_task.responsible_person == "Developer"
    assert "december 5" in auth_task.deadline.lower()
    
    promo_task = next((t for t in result.action_items if "promotional" in t.task_description.lower()), None)
    assert promo_task is not None
    assert promo_task.responsible_person == "Marketing Lead"
    assert "december 8" in promo_task.deadline.lower()

def test_extraction_missing_fields_defaults():
    title = "Vague Meeting"
    date = "2026-12-01"
    participants = "Alice"
    transcript = "Alice: We will complete something sometime."
    
    result, mode = extract_meeting_intelligence(title, date, participants, transcript)
    assert isinstance(result, MeetingExtractionResult)
    for task in result.action_items:
        assert task.responsible_person is not None
        assert task.deadline is not None
        assert task.priority in ["Low", "Medium", "High", "Critical"]

if __name__ == "__main__":
    test_extraction_structure_meeting1()
    test_extraction_missing_fields_defaults()
    print("✅ All extraction tests passed successfully!")
