"""Decision Memory UI component."""
import streamlit as st
import pandas as pd
from meetflow.services.memory_service import get_memory_timeline
from meetflow.database import operations

def render_memory_view():
    st.markdown("### 🏛️ Persistent Organizational Decision Memory")
    st.markdown("MeetFlow AI maintains a long-term, cross-meeting memory of all commitments, policies, and roadmap decisions.")

    timeline = get_memory_timeline()
    if not timeline:
        st.info("No decisions stored in memory yet. Ingest meetings to build organizational memory.")
        return

    # Filter controls
    col_search, col_status = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search Memory across all meetings", placeholder="Search by keyword, decision, or topic...")
    with col_status:
        status_filter = st.selectbox("Filter Status", ["All", "Active", "Superseded", "Conflicted"])

    filtered = timeline
    if search_query:
        filtered = [d for d in filtered if search_query.lower() in d["decision_text"].lower() or search_query.lower() in d["meeting_title"].lower()]
    if status_filter != "All":
        filtered = [d for d in filtered if d["status"] == status_filter]

    st.markdown(f"**Showing {len(filtered)} Historical Decision(s)**")

    for dec in filtered:
        status = dec["status"]
        if status == "Active":
            badge_color = "#10b981"
            border_color = "#10b981"
        elif status == "Superseded":
            badge_color = "#64748b"
            border_color = "#475569"
        else:
            badge_color = "#ef4444"
            border_color = "#ef4444"

        st.markdown(f"""
        <div style="background: #1e293b; border-left: 5px solid {border_color}; border-radius: 8px; padding: 16px; margin-bottom: 12px; border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 13px; font-weight: 700; color: #818cf8;">📁 {dec['meeting_title']} ({dec['meeting_date']})</span>
                <span style="background: {badge_color}22; color: {badge_color}; border: 1px solid {badge_color}; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">{status.upper()}</span>
            </div>
            <div style="font-size: 14px; font-weight: 500; color: #f8fafc; line-height: 1.5;">
                {dec['decision_text']}
            </div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 8px;">
                Category: <b>{dec['category']}</b> | Recorded: {dec['timestamp']}
            </div>
        </div>
        """, unsafe_allow_html=True)
