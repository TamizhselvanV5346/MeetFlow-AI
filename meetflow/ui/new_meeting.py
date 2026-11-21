"""New Meeting Ingestion UI component."""
import streamlit as st
from datetime import date
from meetflow.services.meeting_service import ingest_and_process_meeting

DEMO_MEETING_1_TITLE = "Product Launch Planning"
DEMO_MEETING_1_PARTICIPANTS = "Manager, Developer, Marketing Lead"
DEMO_MEETING_1_TRANSCRIPT = """Manager: We are planning to launch our new product on December 10.
Developer: I will complete the authentication module by December 5.
Marketing Lead: I will prepare the promotional campaign before December 8.
Manager: The development team must complete all testing before launch."""

DEMO_MEETING_2_TITLE = "Product Launch Review"
DEMO_MEETING_2_PARTICIPANTS = "Manager, Developer, Marketing Lead"
DEMO_MEETING_2_TRANSCRIPT = """Manager: Due to development delays, we are postponing the product launch to December 15.
Developer: Authentication testing will require additional time.
Marketing Lead: I will update the promotional campaign according to the new launch date."""

def render_new_meeting():
    st.markdown("### 📥 Ingest Meeting Conversation")
    st.markdown("Submit transcripts to extract structured decisions, action items, dependencies, and verify against historical memory.")

    # Demonstration Scenario Quick-Load Buttons
    st.markdown("#### ⚡ Quick-Load Demonstration Scenario")
    st.info("Click either button below to auto-populate the official two-meeting connected demonstration scenario:")
    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        if st.button("🚀 Load Meeting 1: Product Launch Planning", use_container_width=True):
            st.session_state["form_title"] = DEMO_MEETING_1_TITLE
            st.session_state["form_date"] = date(2026, 12, 1)
            st.session_state["form_participants"] = DEMO_MEETING_1_PARTICIPANTS
            st.session_state["form_transcript"] = DEMO_MEETING_1_TRANSCRIPT
            st.rerun()
    with col_demo2:
        if st.button("🔄 Load Meeting 2: Product Launch Review (Conflict Scenario)", use_container_width=True):
            st.session_state["form_title"] = DEMO_MEETING_2_TITLE
            st.session_state["form_date"] = date(2026, 12, 4)
            st.session_state["form_participants"] = DEMO_MEETING_2_PARTICIPANTS
            st.session_state["form_transcript"] = DEMO_MEETING_2_TRANSCRIPT
            st.rerun()

    st.markdown("---")

    # Ingestion Form
    title_val = st.session_state.get("form_title", "")
    date_val = st.session_state.get("form_date", date.today())
    participants_val = st.session_state.get("form_participants", "")
    transcript_val = st.session_state.get("form_transcript", "")

    c_title, c_date = st.columns([2, 1])
    with c_title:
        meeting_title = st.text_input("Meeting Title *", value=title_val, placeholder="e.g. Q4 Executive Strategy Sync")
    with c_date:
        meeting_date = st.date_input("Meeting Date *", value=date_val)

    participants = st.text_input("Participants *", value=participants_val, placeholder="e.g. Alice (Lead), Bob (Frontend), Charlie (PM)")

    uploaded_file = st.file_uploader("Upload Meeting Transcript (.txt)", type=["txt"])
    if uploaded_file is not None:
        try:
            transcript_val = uploaded_file.read().decode("utf-8")
            st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")

    transcript = st.text_area(
        "Meeting Transcript (Preserve speaker labels if available) *",
        value=transcript_val,
        height=220,
        placeholder="Speaker 1: We decided to...\nSpeaker 2: I will take responsibility for..."
    )

    col_submit, col_clear = st.columns([1, 4])
    with col_submit:
        process_btn = st.button("🚀 Process Transcript with MeetFlow AI", type="primary", use_container_width=True)

    if process_btn:
        if not meeting_title.strip() or not transcript.strip():
            st.error("Please provide both a Meeting Title and Transcript content.")
            return

        with st.spinner("Processing transcript, extracting intelligence, and comparing with organizational memory..."):
            try:
                result = ingest_and_process_meeting(
                    title=meeting_title.strip(),
                    date=str(meeting_date),
                    participants=participants.strip() or "General Participants",
                    transcript=transcript.strip()
                )

                st.session_state["latest_result"] = result
                st.session_state["latest_meeting_title"] = meeting_title.strip()
                st.success(f"Meeting '{meeting_title}' processed successfully!")

                # Check if conflicts were detected
                conflicts = result["conflict_result"].conflicts
                if conflicts:
                    st.warning(f"🚨 **{len(conflicts)} Decision Conflict(s) Detected!** Immediate human review required.")
                    st.session_state["nav_selection"] = "Conflict Detection"
                else:
                    st.session_state["nav_selection"] = "AI Insights"
                st.rerun()

            except Exception as e:
                st.error(f"Failed to process meeting: {str(e)}")
