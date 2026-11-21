"""Custom CSS design system for MeetFlow AI SaaS Interface."""

CUSTOM_CSS = """
<style>
/* Main Container & Font Styles */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header & Banner */
.main-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
    padding: 24px 32px;
    border-radius: 14px;
    color: #ffffff;
    margin-bottom: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
}

.main-header h1 {
    font-size: 28px;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.5px;
    color: #f8fafc;
}

.main-header p {
    font-size: 14px;
    color: #cbd5e1;
    margin-top: 6px;
    margin-bottom: 0;
}

/* Metric KPI Cards */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.kpi-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.kpi-card:hover {
    border-color: #6366f1;
    transform: translateY(-2px);
}

.kpi-title {
    font-size: 12px;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: #94a3b8;
}

.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 6px;
}

.kpi-sub {
    font-size: 11px;
    color: #64748b;
    margin-top: 4px;
}

/* Feature Cards */
.glass-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}

.glass-card-title {
    font-size: 16px;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Conflict Alert Box */
.conflict-card {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-left: 5px solid #ef4444;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 18px;
}

.conflict-badge {
    background: #ef4444;
    color: #ffffff;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    text-transform: uppercase;
}

.badge-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
}

.badge-high {
    background: rgba(239, 68, 68, 0.2);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.4);
}

.badge-medium {
    background: rgba(245, 158, 11, 0.2);
    color: #fcd34d;
    border: 1px solid rgba(245, 158, 11, 0.4);
}

.badge-low {
    background: rgba(16, 185, 129, 0.2);
    color: #86efac;
    border: 1px solid rgba(16, 185, 129, 0.4);
}

.badge-approved {
    background: rgba(16, 185, 129, 0.2);
    color: #34d399;
}

.badge-pending {
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
}

/* Side by side comparison */
.comparison-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 12px;
    margin-bottom: 12px;
}

.comparison-box-historical {
    background: rgba(100, 116, 139, 0.15);
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 14px;
}

.comparison-box-new {
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid #6366f1;
    border-radius: 8px;
    padding: 14px;
}

/* Sidebar Branding */
.sidebar-brand {
    padding: 12px 0 20px 0;
    border-bottom: 1px solid #334155;
    margin-bottom: 16px;
}

.sidebar-brand h2 {
    font-size: 20px;
    font-weight: 700;
    color: #6366f1;
    margin: 0;
}

.sidebar-brand p {
    font-size: 11px;
    color: #94a3b8;
    margin: 2px 0 0 0;
}
</style>
"""
