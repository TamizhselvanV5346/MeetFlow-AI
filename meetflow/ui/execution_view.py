"""Execution Tracker UI component."""
import streamlit as st
import pandas as pd
from meetflow.services.task_service import get_approved_tasks, update_execution_status
from meetflow.database import operations

def render_execution_view():
    st.markdown("### 🚀 Execution Tracker")
    st.markdown("Track and update all human-approved commitments through delivery.")

    approved_tasks = get_approved_tasks()
    if not approved_tasks:
        st.info("No approved tasks are currently in the execution tracker. Review and approve tasks in **Task Approvals**.")
        return

    # Filter row
    f_c1, f_c2, f_c3 = st.columns(3)
    with f_c1:
        status_filter = st.selectbox("Execution Status Filter", ["All", "In Progress", "Completed", "Not Started"])
    with f_c2:
        priority_filter = st.selectbox("Priority Filter", ["All", "Critical", "High", "Medium", "Low"])
    with f_c3:
        search_filter = st.text_input("Search Tasks / Owners", placeholder="Filter by keyword...")

    filtered = approved_tasks
    if status_filter != "All":
        filtered = [t for t in filtered if t["execution_status"] == status_filter]
    if priority_filter != "All":
        filtered = [t for t in filtered if t["priority"] == priority_filter]
    if search_filter:
        filtered = [
            t for t in filtered
            if search_filter.lower() in t["task_description"].lower()
            or search_filter.lower() in t["responsible_person"].lower()
        ]

    st.markdown(f"**Tracking {len(filtered)} Approved Task(s)**")

    # Table summary
    if filtered:
        table_data = []
        for t in filtered:
            table_data.append({
                "Task": t["task_description"],
                "Owner": t["responsible_person"],
                "Deadline": t["deadline"],
                "Priority": t["priority"],
                "Execution Status": t["execution_status"],
                "Source Meeting": t.get("source_meeting_title", "Meeting"),
                "Approved At": t.get("approved_at", "—")
            })
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🔄 Update Task Execution Status")

    for t in filtered:
        t_id = t["id"]
        exec_status = t["execution_status"]
        
        # Priority styling
        prio = t["priority"]
        prio_color = "#ef4444" if prio in ["Critical", "High"] else "#f59e0b" if prio == "Medium" else "#10b981"

        with st.container():
            col_info, col_status_act = st.columns([3, 2])
            with col_info:
                st.markdown(f"""
                <div style="background: #1e293b; padding: 14px; border-radius: 8px; border-left: 4px solid {prio_color}; margin-bottom: 10px;">
                    <div style="font-size: 14px; font-weight: 600; color: #f8fafc;">{t['task_description']}</div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">
                        👤 Owner: <b>{t['responsible_person']}</b> | 📅 Deadline: <b>{t['deadline']}</b> | 
                        🏷️ Priority: <span style="color:{prio_color}; font-weight:700;">{prio}</span> | 
                        Source: {t.get('source_meeting_title', 'Meeting')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_status_act:
                status_choices = ["Not Started", "In Progress", "Completed"]
                curr_idx = status_choices.index(exec_status) if exec_status in status_choices else 0
                new_status = st.selectbox(
                    "Update Status",
                    status_choices,
                    index=curr_idx,
                    key=f"status_sel_{t_id}",
                    label_visibility="collapsed"
                )
                if new_status != exec_status:
                    update_execution_status(t_id, new_status)
                    st.toast(f"Updated '{t['task_description'][:30]}' to {new_status}")
                    st.rerun()
