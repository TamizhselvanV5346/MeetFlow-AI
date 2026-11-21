"""MeetFlow AI: Autonomous Agentic Meeting-to-Execution SaaS Platform.
Main Streamlit application entrypoint.
"""
import streamlit as st
import sys
from pathlib import Path

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from meetflow.config import IS_LIVE_GEMINI, GEMINI_MODEL
from meetflow.ui.styles import CUSTOM_CSS
from meetflow.ui.dashboard import render_dashboard
from meetflow.ui.new_meeting import render_new_meeting
from meetflow.ui.ai_insights import render_ai_insights
from meetflow.ui.memory_view import render_memory_view
from meetflow.ui.conflict_view import render_conflict_view
from meetflow.ui.approvals_view import render_approvals_view
from meetflow.ui.execution_view import render_execution_view
from meetflow.ui.digest_view import render_digest_view
from meetflow.database import operations

# Configure Streamlit page
st.set_page_config(
    page_title="MeetFlow AI — Meeting to Execution SaaS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Main Banner Header
engine_badge = "🟢 Live Gemini 2.5 Flash" if IS_LIVE_GEMINI else "🔵 Demo Engine (Deterministic Agent Pipeline)"

st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>⚡ MeetFlow AI</h1>
            <p>From Meeting Conversations to Measurable Execution — Autonomous Agentic SaaS</p>
        </div>
        <div style="background: rgba(255, 255, 255, 0.15); padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.2);">
            {engine_badge}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>⚡ MeetFlow AI</h2>
        <p>Enterprise Meeting Intelligence & Execution</p>
    </div>
    """, unsafe_allow_html=True)

    # Calculate badge notifications
    conflicts = operations.list_conflicts()
    unresolved_conflicts = len([c for c in conflicts if c["resolution_status"] == "Unresolved"])
    pending_tasks = len(operations.list_action_items(approval_status="Pending"))

    conflict_nav_label = f"5. Conflict Detection ({unresolved_conflicts} ⚠️)" if unresolved_conflicts > 0 else "5. Conflict Detection"
    approval_nav_label = f"6. Task Approvals ({pending_tasks} ⏳)" if pending_tasks > 0 else "6. Task Approvals"

    nav_options = [
        "1. Overview",
        "2. New Meeting",
        "3. AI Insights",
        "4. Decision Memory",
        conflict_nav_label,
        approval_nav_label,
        "7. Execution Tracker",
        "8. Executive Digest"
    ]

    # Map back to simple selection keys
    key_mapping = {
        "1. Overview": "Overview",
        "2. New Meeting": "New Meeting",
        "3. AI Insights": "AI Insights",
        "4. Decision Memory": "Decision Memory",
        conflict_nav_label: "Conflict Detection",
        approval_nav_label: "Task Approvals",
        "7. Execution Tracker": "Execution Tracker",
        "8. Executive Digest": "Executive Digest"
    }

    current_selection = st.session_state.get("nav_selection", "Overview")
    # Find matching option index
    default_idx = 0
    for idx, opt in enumerate(nav_options):
        if key_mapping.get(opt) == current_selection:
            default_idx = idx
            break

    selected_nav = st.radio("Navigation", nav_options, index=default_idx)
    st.session_state["nav_selection"] = key_mapping[selected_nav]

    st.markdown("---")
    st.markdown("### ⚙️ Demo Controls")
    if st.button("🧹 Reset Database (Clean Demo)", use_container_width=True):
        operations.reset_all_data()
        st.session_state.clear()
        st.toast("Database reset to clean state.")
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 11px; color: #64748b; line-height: 1.4;">
            <b>Core Innovation:</b><br>
            • Persistent Cross-Meeting Memory<br>
            • Decision Conflict Detection<br>
            • Human-in-the-Loop Execution
        </div>
        """,
        unsafe_allow_html=True
    )

# Page Routing
page = st.session_state.get("nav_selection", "Overview")

if page == "Overview":
    render_dashboard()
elif page == "New Meeting":
    render_new_meeting()
elif page == "AI Insights":
    render_ai_insights()
elif page == "Decision Memory":
    render_memory_view()
elif page == "Conflict Detection":
    render_conflict_view()
elif page == "Task Approvals":
    render_approvals_view()
elif page == "Execution Tracker":
    render_execution_view()
elif page == "Executive Digest":
    render_digest_view()
