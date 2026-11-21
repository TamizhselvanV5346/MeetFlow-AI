"""Decision Conflict Detection UI component."""
import streamlit as st
from meetflow.services.conflict_service import get_all_conflicts, resolve_conflict
from meetflow.database import operations

def render_conflict_view():
    st.markdown("### 🛡️ Decision Conflict Detection & Resolution")
    st.markdown("MeetFlow AI's signature capability: cross-meeting contradiction detection protecting organizational integrity.")

    conflicts = get_all_conflicts()
    if not conflicts:
        st.success("🎉 No decision conflicts detected in organizational memory. All commitments are aligned!")
        st.info("Tip: Ingest **Meeting 1 (Product Launch Planning - Dec 10)** followed by **Meeting 2 (Product Launch Review - Postponed to Dec 15)** to witness real-time conflict detection.")
        return

    # Filter selector
    filter_col1, filter_col2 = st.columns([1, 2])
    with filter_col1:
        status_filter = st.selectbox("Resolution Filter", ["All", "Unresolved", "Confirmed Update", "Rejected"])
    
    filtered_conflicts = conflicts
    if status_filter != "All":
        filtered_conflicts = [c for c in conflicts if c["resolution_status"] == status_filter]

    st.markdown(f"**Showing {len(filtered_conflicts)} Decision Conflict Record(s)**")

    for c in filtered_conflicts:
        c_id = c["id"]
        res_status = c["resolution_status"]

        if res_status == "Unresolved":
            border_style = "border-left: 6px solid #ef4444;"
            status_badge = '<span style="background:#ef4444; color:#fff; font-size:11px; font-weight:700; padding:3px 8px; border-radius:4px;">NEEDS REVIEW</span>'
        elif res_status == "Confirmed Update":
            border_style = "border-left: 6px solid #10b981;"
            status_badge = '<span style="background:#10b981; color:#fff; font-size:11px; font-weight:700; padding:3px 8px; border-radius:4px;">CONFIRMED UPDATE</span>'
        else:
            border_style = "border-left: 6px solid #64748b;"
            status_badge = '<span style="background:#64748b; color:#fff; font-size:11px; font-weight:700; padding:3px 8px; border-radius:4px;">REJECTED</span>'

        st.markdown(f"""
        <div style="background: #1e293b; {border_style} border-radius: 10px; padding: 20px; margin-bottom: 20px; border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 14px; font-weight: 700; color: #f87171;">⚠️ CONFLICT DETECTED: {c['conflict_type']}</span>
                <div>{status_badge}</div>
            </div>
            
            <div style="color: #cbd5e1; font-size: 13px; margin-bottom: 14px; line-height: 1.5;">
                <b>Analysis:</b> {c['explanation']}
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px;">
                <div style="background: rgba(100, 116, 139, 0.15); border: 1px solid #475569; border-radius: 8px; padding: 12px;">
                    <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #94a3b8; margin-bottom: 4px;">⏮️ Historical Decision in Memory</div>
                    <div style="font-size: 13px; font-weight: 600; color: #f1f5f9;">{c['historical_decision_text']}</div>
                </div>
                <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid #6366f1; border-radius: 8px; padding: 12px;">
                    <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #818cf8; margin-bottom: 4px;">🆕 Proposed New Decision</div>
                    <div style="font-size: 13px; font-weight: 600; color: #ffffff;">{c['new_decision_text']}</div>
                </div>
            </div>

            <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 6px; padding: 10px 14px; font-size: 12px; color: #fcd34d; margin-bottom: 14px;">
                <b>💡 Recommended Action:</b> {c['recommended_action']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Action resolution buttons
        col_btn1, col_btn2, col_btn3, _ = st.columns([1.2, 1, 1, 2])
        with col_btn1:
            if st.button("✅ Confirm Update", key=f"conf_up_{c_id}", use_container_width=True, type="primary"):
                resolve_conflict(c_id, "Confirmed Update", historical_decision_id=c.get("historical_decision_id"))
                st.success("Conflict resolved: Confirmed update saved. Historical decision marked as Superseded.")
                st.rerun()
        with col_btn2:
            if st.button("❌ Reject Proposal", key=f"conf_rej_{c_id}", use_container_width=True):
                resolve_conflict(c_id, "Rejected", historical_decision_id=c.get("historical_decision_id"))
                st.warning("Conflict rejected: Historical decision maintained as active.")
                st.rerun()
        with col_btn3:
            if st.button("⏳ Mark Unresolved", key=f"conf_unres_{c_id}", use_container_width=True):
                resolve_conflict(c_id, "Unresolved", historical_decision_id=c.get("historical_decision_id"))
                st.info("Conflict flagged as Unresolved for management review.")
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
