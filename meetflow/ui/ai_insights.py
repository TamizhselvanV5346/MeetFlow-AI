"""AI Insights UI component."""
import streamlit as st
import pandas as pd
from meetflow.database import operations

def render_ai_insights():
    st.markdown("### 🧠 AI Meeting Intelligence")
    st.markdown("Structured decisions, actionable tasks, dependencies, and questions extracted from meeting conversations.")

    # Meeting Selector
    meetings = operations.list_meetings()
    if not meetings:
        st.info("No meetings ingested yet. Ingest a transcript via the **New Meeting** tab.")
        return

    meeting_options = {f"{m['title']} ({m['date']})": m["id"] for m in meetings}
    selected_label = st.selectbox("Select Meeting to Inspect:", list(meeting_options.keys()))
    selected_id = meeting_options[selected_label]
    meeting = operations.get_meeting(selected_id)

    # Engine badge
    latest_result = st.session_state.get("latest_result")
    if latest_result and latest_result.get("meeting_id") == selected_id:
        mode = latest_result.get("engine_mode", "LIVE_GEMINI")
        badge_color = "#10b981" if mode == "LIVE_GEMINI" else "#6366f1"
        st.markdown(
            f"""<div style="display:inline-block; background:{badge_color}22; color:{badge_color}; border:1px solid {badge_color}; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600; margin-bottom:15px;">
            Engine Mode: {mode} (Pydantic Schema Validated)
            </div>""",
            unsafe_allow_html=True
        )

    # Executive Summary Card
    st.markdown(f"""
    <div class="glass-card">
        <div class="glass-card-title">📋 Executive Summary</div>
        <p style="color: #cbd5e1; font-size: 14px; line-height: 1.6; margin: 0;">{meeting['summary'] or 'Summary not available.'}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🎯 Decisions Agreed Upon")
        decisions = operations.list_decisions(meeting_id=selected_id)
        if decisions:
            for d in decisions:
                status_color = "#10b981" if d["status"] == "Active" else "#ef4444"
                st.markdown(f"""
                <div style="background: #1e293b; border-left: 4px solid {status_color}; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
                    <div style="font-size: 13px; font-weight: 600; color: #f8fafc;">{d['decision_text']}</div>
                    <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Status: <b>{d['status']}</b> | Category: {d['category']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No explicit decisions identified for this meeting.")

        st.markdown("#### 🔗 Dependencies")
        deps = meeting.get("dependencies", [])
        if deps:
            for dep in deps:
                st.markdown(f"• {dep}")
        else:
            st.info("No critical cross-team dependencies flagged.")

    with col2:
        st.markdown("#### 📌 Key Discussion Points")
        points = meeting.get("discussion_points", [])
        if points:
            for pt in points:
                st.markdown(f"• {pt}")
        else:
            st.info("No key discussion points recorded.")

        st.markdown("#### ❓ Unresolved Questions")
        unresolved = meeting.get("unresolved_questions", [])
        if unresolved:
            for q in unresolved:
                st.markdown(f"❓ *{q}*")
        else:
            st.info("No open questions remained at meeting close.")

    st.markdown("---")
    st.markdown("#### 📋 Extracted Action Items for This Meeting")
    tasks = operations.list_action_items(meeting_id=selected_id)
    if tasks:
        df = pd.DataFrame(tasks)[["task_description", "responsible_person", "deadline", "priority", "approval_status"]]
        df.columns = ["Task Description", "Owner", "Deadline", "Priority", "Approval Status"]
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        c_app, _ = st.columns([1, 3])
        with c_app:
            if st.button("👉 Proceed to Human-in-the-Loop Task Approvals", type="primary"):
                st.session_state["nav_selection"] = "Task Approvals"
                st.rerun()
    else:
        st.info("No action items extracted for this meeting.")
