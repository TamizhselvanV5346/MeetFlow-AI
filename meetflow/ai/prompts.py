"""Prompt templates for MeetFlow AI extraction and conflict detection."""

MEETING_EXTRACTION_PROMPT = """You are MeetFlow AI's Lead Intelligence Agent.
Analyze the following meeting transcript and extract structured intelligence.

Meeting Title: {title}
Meeting Date: {date}
Participants: {participants}

Raw Transcript:
{transcript}

Rules:
1. Extract an executive summary of what transpired.
2. List important discussion points.
3. Extract all explicit decisions made. Do not invent decisions not supported by the transcript.
4. Extract all actionable tasks. For each task, extract:
   - task_description: Concise actionable task
   - responsible_person: Name or role. If not clearly stated, use "Unassigned"
   - deadline: Deadline or date mentioned. If missing, use "Unknown"
   - priority: "Low", "Medium", "High", or "Critical"
5. List any team or technical dependencies.
6. List unresolved questions or open topics requiring follow-up.

Return output strictly conforming to the requested JSON schema.
"""

CONFLICT_DETECTION_PROMPT = """You are MeetFlow AI's Persistent Memory & Decision Conflict Detection Agent.
Your role is to protect organizational integrity by comparing NEW decisions from the current meeting against HISTORICAL decisions from previous meetings.

Current Meeting Title: {current_title}
Current Meeting Date: {current_date}

Newly Proposed Decisions in Current Meeting:
{new_decisions_json}

Historical Decisions from Previous Meetings in Persistent Memory:
{historical_decisions_json}

Task:
Compare each new decision with historical decisions.
Detect any:
1. Direct contradictions
2. Changed deadlines (e.g., launch postponed or moved up)
3. Changed responsibilities (e.g., owner transferred)
4. Cancelled decisions
5. Reversed decisions
6. Potentially conflicting commitments

For any detected conflict:
- Provide historical_decision_text
- Provide new_decision_text
- Classify conflict_type as one of:
  "Deadline Modification", "Responsibility Reassignment", "Contradiction", "Cancellation", "Reversal", "Potentially Conflicting Commitment"
- Provide an explanation of the contradiction
- Suggest a recommended_action

If no conflicts exist, return an empty list of conflicts.
Return output strictly conforming to the requested JSON schema.
"""
