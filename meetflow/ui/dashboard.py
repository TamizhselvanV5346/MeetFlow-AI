"""Dashboard Overview UI component."""
import streamlit as st
import pandas as pd
from meetflow.services.task_service import get_dashboard_metrics, get_weekly_digest
from meetflow.database import operations

def render_dashboard():
    st.markdown("### 📊 Executive Execution Overview")
    st.markdown("Real-time persistent intelligence across organizational meetings, decisions, and task execution.")

    metrics = get_dashboard_metrics()

    # KPI Metrics Row 1
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Total Meetings Ingested", value=metrics["total_meetings"], help="Meetings processed into persistent memory")
    with c2:
        st.metric(label="Decisions Captured", value=metrics["total_decisions"], help="Decisions preserved in organizational memory")
    with c3:
        st.metric(label="Extracted Action Items", value=metrics["total_tasks"], help="Total tasks extracted across all meetings")
    with c4:
        st.metric(label="Pending Human Approvals", value=metrics["pending_approvals"], delta=f"-{metrics['pending_approvals']}" if metrics['pending_approvals'] > 0 else "All Approved", delta_color="inverse")

    # KPI Metrics Row 2
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.metric(label="Approved Tasks", value=metrics["approved_tasks"])
    with c6:
        st.metric(label="Completed Tasks", value=metrics["completed_tasks"])
    with c7:
        st.metric(label="Overdue / Critical", value=metrics["overdue_tasks"], delta="Attention Required" if metrics["overdue_tasks"] > 0 else "On Track", delta_color="inverse")
    with c8:
        st.metric(label="Active Decision Conflicts", value=metrics["unresolved_conflicts"], delta="Needs Resolution" if metrics["unresolved_conflicts"] > 0 else "Harmonized", delta_color="inverse")

    st.markdown("---")

    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.markdown("#### ⚡ Execution Pipeline Progress")
        approved_tasks = operations.list_action_items(approval_status="Approved")
        if approved_tasks:
            df = pd.DataFrame(approved_tasks)[["task_description", "responsible_person", "deadline", "priority", "execution_status"]]
            df.columns = ["Task", "Owner", "Deadline", "Priority", "Status"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No approved tasks in the execution tracker yet. Ingest a meeting and approve tasks in **Task Approvals**.")

    with col_right:
        st.markdown("#### 🛡️ Decision Conflict Monitor")
        conflicts = operations.list_conflicts()
        unresolved = [c for c in conflicts if c["resolution_status"] == "Unresolved"]
        if unresolved:
            st.error(f"🚨 **{len(unresolved)} Decision Conflict(s) Flagged!**")
            for c in unresolved[:3]:
                st.markdown(f"""
                <div class="conflict-card">
                    <span class="conflict-badge">{c['conflict_type']}</span>
                    <p style="margin-top: 8px; font-size: 13px; color: #f8fafc;"><b>New Proposal:</b> {c['new_decision_text']}</p>
                    <p style="font-size: 12px; color: #cbd5e1;"><b>Historical Decision:</b> {c['historical_decision_text']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Organizational memory is in harmony. No unaddressed decision conflicts.")

        st.markdown("#### 📅 Quick Actions")
        if st.button("➕ Ingest New Meeting Transcript", use_container_width=True, type="primary"):
            st.session_state["nav_selection"] = "New Meeting"
            st.rerun()
