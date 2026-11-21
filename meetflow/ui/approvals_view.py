"""Human-in-the-Loop Task Approvals UI component."""
import streamlit as st
from meetflow.services.task_service import get_pending_tasks, approve_task, reject_task, edit_task
from meetflow.database import operations

def render_approvals_view():
    st.markdown("### ✍️ Human-in-the-Loop Task Approvals")
    st.markdown("No autonomous task is promoted to execution without explicit human verification and sign-off.")

    pending_tasks = get_pending_tasks()
    if not pending_tasks:
        st.success("🎉 All extracted tasks have been reviewed! No pending approvals.")
        st.info("Ingest new meeting transcripts to generate more action items, or inspect approved items in the **Execution Tracker**.")
        return

    st.markdown(f"**Found {len(pending_tasks)} Action Item(s) Awaiting Review**")
    
    col_batch1, col_batch2, _ = st.columns([1.5, 1.5, 3])
    with col_batch1:
        if st.button("✅ Approve All Pending Tasks", type="primary", use_container_width=True):
            for t in pending_tasks:
                approve_task(t["id"])
            st.success("All pending action items approved and dispatched to Execution Tracker!")
            st.rerun()
    with col_batch2:
        if st.button("❌ Reject All Pending Tasks", use_container_width=True):
            for t in pending_tasks:
                reject_task(t["id"])
            st.warning("All pending action items marked as Rejected.")
            st.rerun()

    st.markdown("---")

    for t in pending_tasks:
        t_id = t["id"]
        source_title = t.get("source_meeting_title") or "Meeting"
        
        with st.expander(f"📌 {t['task_description']} — [Owner: {t['responsible_person']} | Deadline: {t['deadline']}]", expanded=True):
            st.markdown(f"<div style='font-size:12px; color:#818cf8; margin-bottom:8px;'>Source: <b>{source_title}</b></div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([2, 1])
            with c1:
                new_desc = st.text_input("Task Description", value=t["task_description"], key=f"desc_{t_id}")
            with c2:
                new_owner = st.text_input("Responsible Owner", value=t["responsible_person"], key=f"owner_{t_id}")

            c3, c4 = st.columns(2)
            with c3:
                new_deadline = st.text_input("Deadline", value=t["deadline"], key=f"dl_{t_id}")
            with c4:
                priority_options = ["Low", "Medium", "High", "Critical"]
                current_prio_idx = priority_options.index(t["priority"]) if t["priority"] in priority_options else 1
                new_prio = st.selectbox("Priority", priority_options, index=current_prio_idx, key=f"prio_{t_id}")

            # Inline Save, Approve, Reject actions
            btn_save, btn_appr, btn_rej, _ = st.columns([1, 1, 1, 2])
            with btn_save:
                if st.button("💾 Save Edits", key=f"save_{t_id}", use_container_width=True):
                    edit_task(t_id, new_desc, new_owner, new_deadline, new_prio)
                    st.success("Task details updated!")
                    st.rerun()
            with btn_appr:
                if st.button("✅ Approve Task", key=f"appr_{t_id}", type="primary", use_container_width=True):
                    # Save any edits first, then approve
                    edit_task(t_id, new_desc, new_owner, new_deadline, new_prio)
                    approve_task(t_id)
                    st.success(f"Task '{new_desc}' approved and moved to Execution Tracker!")
                    st.rerun()
            with btn_rej:
                if st.button("❌ Reject", key=f"rej_{t_id}", use_container_width=True):
                    reject_task(t_id)
                    st.warning("Task rejected.")
                    st.rerun()
