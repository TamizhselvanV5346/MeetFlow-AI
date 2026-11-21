"""Reminder & Weekly Digest UI component."""
import streamlit as st
from datetime import datetime, date
from meetflow.services.task_service import get_weekly_digest, get_approved_tasks, get_dashboard_metrics

def render_digest_view():
    st.markdown("### 📬 Executive Digest & Deadline Reminders")
    st.markdown("Automated deadline monitoring and executive weekly execution synthesis.")

    metrics = get_dashboard_metrics()
    digest = get_weekly_digest()

    st.markdown("#### ⏰ Active Deadline Monitor")
    d_c1, d_c2, d_c3 = st.columns(3)
    with d_c1:
        st.metric(label="Tasks Due Today", value=metrics["due_today_tasks"])
    with d_c2:
        st.metric(label="Upcoming Deadlines", value=metrics["upcoming_deadlines"])
    with d_c3:
        st.metric(label="Overdue / Critical Items", value=metrics["overdue_tasks"], delta="Review Now" if metrics["overdue_tasks"] > 0 else "All On Time", delta_color="inverse")

    st.markdown("---")
    st.markdown("#### 📑 Generate Weekly Execution Digest")
    
    if st.button("✨ Synthesize Executive Weekly Digest", type="primary"):
        st.session_state["show_digest"] = True

    if st.session_state.get("show_digest", True):
        active_tasks = digest.get("active_tasks", [])
        decisions = digest.get("recent_decisions", [])
        
        digest_md = f"""# 📈 MeetFlow AI Executive Digest
**Generated:** {digest['generated_at']}
**Platform:** MeetFlow AI SaaS Intelligence Platform

---

### 1. Executive Summary KPIs
- **Total Ingested Meetings:** {digest['total_meetings']}
- **Total Decisions in Organizational Memory:** {digest['total_decisions']}
- **Tasks Approved & In Execution:** {digest['approved_tasks_count']}
- **Completed Execution Items:** {digest['completed_tasks_count']}
- **Pending Human Approvals:** {digest['pending_approvals_count']}
- **Decision Conflicts Flagged:** {digest['total_conflicts_flagged']} ({digest['unresolved_conflicts']} Unresolved)

---

### 2. Recent Key Decisions
"""
        for d in decisions:
            digest_md += f"- **[{d.get('category', 'General')}]** {d.get('decision_text')} *(Source: {d.get('source_meeting_title', 'Meeting')})*\n"

        digest_md += "\n---\n\n### 3. Active Execution Deliverables\n"
        for t in active_tasks:
            digest_md += f"- [{t.get('execution_status')}] **{t.get('task_description')}** | Owner: `{t.get('responsible_person')}` | Deadline: `{t.get('deadline')}` | Priority: `{t.get('priority')}`\n"

        st.markdown(f"""
        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 24px; margin-top: 16px;">
        """, unsafe_allow_html=True)
        
        st.markdown(digest_md)
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Digest Markdown (.md)",
            data=digest_md,
            file_name=f"MeetFlow_Weekly_Digest_{date.today().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
