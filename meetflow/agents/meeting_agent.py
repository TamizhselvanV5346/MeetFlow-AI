"""Meeting Agent: Orchestrates transcript processing and extraction."""
from typing import Dict, Any, Tuple
from meetflow.ai.extraction import extract_meeting_intelligence
from meetflow.ai.schemas import MeetingExtractionResult

class MeetingAgent:
    """Agent responsible for meeting ingestion and LLM intelligence extraction."""
    
    def process_transcript(
        self,
        title: str,
        date: str,
        participants: str,
        transcript: str
    ) -> Tuple[MeetingExtractionResult, str]:
        """
        Extract structured decisions, action items, summaries, and open questions.
        Returns: (MeetingExtractionResult, extraction_engine_mode)
        """
        if not transcript or not transcript.strip():
            raise ValueError("Meeting transcript cannot be empty.")
            
        return extract_meeting_intelligence(
            title=title,
            date=date,
            participants=participants,
            transcript=transcript
        )
