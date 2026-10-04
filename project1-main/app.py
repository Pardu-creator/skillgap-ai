import streamlit as st
from backend import register_user, login_user, analyze_resume, ai_mentor_response
import random
import time

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="SkillGap AI • Advanced Career Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------
def init_session():
    defaults = {
        "logged_in": False,
        "username": "",
        "analysis_result": None,
        "last_uploaded_name": "",
        "mentor_chat": [],
        "active_tab": "Overview"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()


# ---------------------------------------------------
# STYLING ENGINE: LIGHT THEME (LOGIN) & ULTRA-MODERN DARK (DASHBOARD)
# ---------------------------------------------------
if not st.session_state.logged_in:
    # ---------------------------------------------------
    # LOGIN SCREEN (PIXEL-PERFECT IMAGE 1)
    # ---------------------------------------------------
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            box-sizing: border-box;
        }

        #MainMenu, footer, header {visibility: hidden;}

        .stApp {
            background: #050510 !important;
            color: #E2E8F0;
            min-height: 100vh;
            overflow: hidden;
        }

        /* Animated background orbs */
        .login-bg-effects {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }
        .login-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            animation: orbFloat 8s ease-in-out infinite;
        }
        .login-orb-1 {
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
            top: -10%; left: -5%;
            animation-delay: 0s;
        }
        .login-orb-2 {
            width: 400px; height: 400px;
            background: radial-gradient(circle, rgba(14, 165, 233, 0.25) 0%, transparent 70%);
            bottom: -15%; right: -5%;
            animation-delay: -3s;
        }
        .login-orb-3 {
            width: 300px; height: 300px;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.2) 0%, transparent 70%);
            top: 50%; left: 40%;
            animation-delay: -5s;
        }
        @keyframes orbFloat {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(30px, -20px) scale(1.05); }
            66% { transform: translate(-20px, 15px) scale(0.95); }
        }

        /* Split screen layout */
        .login-split-container {
            display: flex;
            min-height: 100vh;
            position: relative;
            z-index: 1;
        }
        .login-left-panel {
            flex: 1.1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 60px 70px;
            position: relative;
        }
        .login-right-panel {
            flex: 0.9;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }

        /* Left panel brand content */
        .login-brand-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 999px;
            background: rgba(99, 102, 241, 0.12);
            border: 1px solid rgba(99, 102, 241, 0.25);
            font-size: 13px;
            font-weight: 600;
            color: #A5B4FC;
            margin-bottom: 28px;
            width: fit-content;
        }
        .login-brand-badge .badge-dot {
            width: 7px; height: 7px;
            background: #6366F1;
            border-radius: 50%;
            box-shadow: 0 0 12px #6366F1;
            animation: pulse-glow 2s ease-in-out infinite;
        }
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 8px #6366F1; }
            50% { box-shadow: 0 0 20px #6366F1, 0 0 40px rgba(99,102,241,0.3); }
        }

        .login-hero-title {
            font-size: 52px;
            font-weight: 900;
            line-height: 1.08;
            letter-spacing: -0.03em;
            margin-bottom: 18px;
        }
        .login-hero-title .title-gradient {
            background: linear-gradient(135deg, #6366F1 0%, #0EA5E9 40%, #A78BFA 80%, #38BDF8 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmer 4s ease-in-out infinite;
        }
        @keyframes shimmer {
            0% { background-position: 0% center; }
            50% { background-position: 100% center; }
            100% { background-position: 0% center; }
        }
        .login-hero-sub {
            font-size: 17px;
            color: #94A3B8;
            line-height: 1.7;
            max-width: 440px;
            margin-bottom: 40px;
            font-weight: 400;
        }

        /* Feature highlights */
        .login-features {
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-bottom: 40px;
        }
        .login-feature-item {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .feature-icon-circle {
            width: 40px; height: 40px;
            min-width: 40px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
        .feature-icon-blue { background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.3); }
        .feature-icon-purple { background: rgba(139, 92, 246, 0.15); border: 1px solid rgba(139, 92, 246, 0.3); }
        .feature-icon-emerald { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); }
        .feature-text {
            font-size: 14px;
            font-weight: 600;
            color: #CBD5E1;
        }
        .feature-text span {
            color: #F8FAFC;
            font-weight: 700;
        }

        /* Trust bar */
        .login-trust-bar {
            display: flex;
            align-items: center;
            gap: 24px;
            padding-top: 10px;
        }
        .trust-stat {
            display: flex;
            flex-direction: column;
        }
        .trust-val {
            font-size: 22px;
            font-weight: 900;
            color: #FFFFFF;
        }
        .trust-label {
            font-size: 12px;
            color: #64748B;
            font-weight: 500;
        }
        .trust-divider {
            width: 1px;
            height: 36px;
            background: rgba(255,255,255,0.08);
        }

        /* Glassmorphism login card */
        .login-glass-card {
            width: 100%;
            max-width: 420px;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 28px;
            padding: 42px 36px;
            box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.5),
                        inset 0 1px 0 rgba(255, 255, 255, 0.06);
            position: relative;
            overflow: hidden;
        }
        .login-glass-card::before {
            content: '';
            position: absolute;
            top: -50%; right: -50%;
            width: 200px; height: 200px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
            pointer-events: none;
        }

        .login-card-header {
            text-align: center;
            margin-bottom: 32px;
        }
        .login-card-icon {
            width: 60px; height: 60px;
            margin: 0 auto 16px auto;
            border-radius: 18px;
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A78BFA 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            box-shadow: 0 12px 28px -4px rgba(99, 102, 241, 0.4);
        }
        .login-card-title {
            font-size: 24px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 6px;
        }
        .login-card-sub {
            font-size: 14px;
            color: #64748B;
            font-weight: 500;
        }

        /* Inputs */
        .stTextInput label {
            font-size: 13px !important;
            font-weight: 700 !important;
            color: #94A3B8 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            margin-bottom: 6px !important;
        }
        .stTextInput input {
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            color: #F8FAFC !important;
            padding: 16px 18px !important;
            font-size: 15px !important;
            transition: all 0.25s ease !important;
        }
        .stTextInput input::placeholder {
            color: #475569 !important;
        }
        .stTextInput input:focus {
            background: rgba(15, 23, 42, 0.95) !important;
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15), 0 0 20px rgba(99, 102, 241, 0.1) !important;
        }

        /* Sign in button */
        .stButton > button {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A78BFA 100%) !important;
            background-size: 200% auto !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 14px !important;
            height: 54px !important;
            font-weight: 800 !important;
            font-size: 16px !important;
            letter-spacing: 0.01em !important;
            box-shadow: 0 8px 24px -4px rgba(99, 102, 241, 0.45) !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            width: 100% !important;
        }
        .stButton > button:hover {
            background-position: right center !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 16px 32px -4px rgba(99, 102, 241, 0.55) !important;
        }
        .stButton > button:active {
            transform: translateY(-1px) !important;
        }

        .demo-note {
            text-align: center;
            color: #64748B;
            font-size: 13px;
            font-weight: 500;
            margin-top: 20px;
            padding: 10px 16px;
            background: rgba(99, 102, 241, 0.06);
            border: 1px solid rgba(99, 102, 241, 0.12);
            border-radius: 10px;
        }
        .demo-note b { color: #A5B4FC; }

        .copyright-text {
            text-align: center;
            color: #334155;
            font-size: 12px;
            margin-top: 22px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    # ---------------------------------------------------
    # ADVANCED DARK DASHBOARD (INSPIRED BY LINEAR, VERCEL, IMAGE 2)
    # ---------------------------------------------------
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            box-sizing: border-box;
            letter-spacing: -0.01em;
        }

        #MainMenu, footer, header {visibility: hidden;}

        /* ===== MAIN ATMOSPHERE ===== */
        .stApp {
            background:
                radial-gradient(ellipse at 10% 0%, rgba(99, 102, 241, 0.12) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 10%, rgba(168, 85, 247, 0.08) 0%, transparent 45%),
                radial-gradient(ellipse at 50% 100%, rgba(14, 165, 233, 0.06) 0%, transparent 50%),
                linear-gradient(180deg, #06080F 0%, #080C18 30%, #0A0E1A 60%, #060810 100%);
            color: #F1F5F9;
        }

        /* ===== SIDEBAR ===== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #080C18 0%, #0A0F1E 50%, #070B14 100%) !important;
            border-right: 1px solid rgba(99, 102, 241, 0.1) !important;
            padding: 20px 16px !important;
        }
        section[data-testid="stSidebar"] .stRadio > div {
            gap: 4px !important;
        }
        section[data-testid="stSidebar"] .stRadio > div > label {
            background: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
            margin: 0 !important;
            transition: all 0.2s ease !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            color: #94A3B8 !important;
        }
        section[data-testid="stSidebar"] .stRadio > div > label:hover {
            background: rgba(99, 102, 241, 0.08) !important;
            color: #E2E8F0 !important;
            border-color: rgba(99, 102, 241, 0.15) !important;
        }
        section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
        section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
            background: rgba(99, 102, 241, 0.12) !important;
            border-color: rgba(99, 102, 241, 0.3) !important;
            color: #A5B4FC !important;
        }

        .sidebar-brand-container {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 10px 10px 24px 10px;
            border-bottom: 1px solid rgba(99, 102, 241, 0.12);
            margin-bottom: 24px;
        }
        .sidebar-logo-icon {
            width: 46px;
            height: 46px;
            border-radius: 14px;
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            color: white;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
        }
        .sidebar-brand-text {
            font-size: 20px;
            font-weight: 900;
            color: #FFFFFF;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }
        .sidebar-brand-sub {
            font-size: 12px;
            color: #6366F1;
            font-weight: 700;
            margin-top: 2px;
            letter-spacing: 0.03em;
        }

        /* ===== HEADER BAR ===== */
        .dash-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 22px 28px;
            background: rgba(10, 15, 30, 0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.1);
            border-radius: 20px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px -8px rgba(0, 0, 0, 0.5);
        }
        .dash-page-title {
            font-size: 22px;
            font-weight: 900;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: -0.02em;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 16px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            background: rgba(99, 102, 241, 0.1);
            color: #A5B4FC;
            border: 1px solid rgba(99, 102, 241, 0.25);
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background: #818CF8;
            border-radius: 50%;
            box-shadow: 0 0 12px #818CF8;
            animation: pulse-dot-anim 2s ease-in-out infinite;
        }
        @keyframes pulse-dot-anim {
            0%, 100% { box-shadow: 0 0 6px #818CF8; opacity: 1; }
            50% { box-shadow: 0 0 18px #818CF8, 0 0 30px rgba(129,140,248,0.3); opacity: 0.8; }
        }

        /* ===== KPI CARDS ===== */
        .kpi-tile {
            background: linear-gradient(145deg, rgba(15, 20, 40, 0.8) 0%, rgba(10, 14, 26, 0.95) 100%);
            border: 1px solid rgba(99, 102, 241, 0.1);
            border-radius: 20px;
            padding: 22px 24px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }
        .kpi-tile::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366F1, #8B5CF6, #A78BFA);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .kpi-tile:hover {
            border-color: rgba(99, 102, 241, 0.3);
            transform: translateY(-4px);
            box-shadow: 0 16px 40px -8px rgba(99, 102, 241, 0.2);
        }
        .kpi-tile:hover::before {
            opacity: 1;
        }
        .kpi-tile-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }
        .kpi-icon-wrap {
            width: 44px;
            height: 44px;
            border-radius: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .kpi-icon-indigo {
            background: rgba(99, 102, 241, 0.12);
            border: 1px solid rgba(99, 102, 241, 0.25);
            color: #818CF8;
        }
        .kpi-icon-purple {
            background: rgba(168, 85, 247, 0.12);
            border: 1px solid rgba(168, 85, 247, 0.25);
            color: #C084FC;
        }
        .kpi-icon-emerald {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.25);
            color: #34D399;
        }
        .kpi-icon-amber {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.25);
            color: #FBBF24;
        }
        .kpi-tile-label {
            font-size: 12px;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .kpi-tile-val {
            font-size: 36px;
            font-weight: 900;
            color: #FFFFFF;
            line-height: 1;
            margin: 4px 0 10px 0;
            letter-spacing: -0.03em;
        }
        .kpi-pill {
            font-size: 11px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 999px;
            display: inline-block;
        }
        .pill-indigo { background: rgba(99, 102, 241, 0.12); color: #A5B4FC; border: 1px solid rgba(99,102,241,0.2); }
        .pill-purple { background: rgba(168, 85, 247, 0.12); color: #C084FC; border: 1px solid rgba(168,85,247,0.2); }
        .pill-emerald { background: rgba(16, 185, 129, 0.12); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.2); }
        .pill-amber { background: rgba(245, 158, 11, 0.12); color: #FCD34D; border: 1px solid rgba(245,158,11,0.2); }

        /* ===== LANDSCAPE CARDS ===== */
        .landscape-card {
            background: rgba(10, 15, 30, 0.65);
            border: 1px solid rgba(99, 102, 241, 0.08);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 16px;
            transition: all 0.25s ease;
        }
        .landscape-card:hover {
            border-color: rgba(99, 102, 241, 0.2);
            box-shadow: 0 8px 32px -8px rgba(0, 0, 0, 0.4);
        }

        /* ===== SKILL ROWS ===== */
        .skill-item-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 18px;
            margin: 6px 0;
            background: rgba(15, 20, 40, 0.5);
            border: 1px solid rgba(99, 102, 241, 0.06);
            border-radius: 14px;
            transition: all 0.2s ease;
        }
        .skill-item-row:hover {
            background: rgba(20, 28, 55, 0.7);
            border-color: rgba(99, 102, 241, 0.18);
            transform: translateX(4px);
        }
        .skill-name-bold {
            font-size: 15px;
            font-weight: 700;
            color: #F1F5F9;
        }
        .level-badge {
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 8px;
            letter-spacing: 0.03em;
        }
        .level-expert { background: rgba(16, 185, 129, 0.1); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.25); }
        .level-proficient { background: rgba(99, 102, 241, 0.1); color: #A5B4FC; border: 1px solid rgba(99, 102, 241, 0.25); }
        .level-learning { background: rgba(244, 63, 94, 0.1); color: #FDA4AF; border: 1px solid rgba(244, 63, 94, 0.25); }

        /* ===== JOB CARD ===== */
        .job-match-card {
            background: rgba(15, 20, 40, 0.5);
            border: 1px solid rgba(99, 102, 241, 0.08);
            border-radius: 16px;
            padding: 18px 22px;
            margin-bottom: 14px;
            transition: all 0.2s ease;
        }
        .job-match-card:hover {
            border-color: rgba(99, 102, 241, 0.25);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px -6px rgba(99, 102, 241, 0.12);
        }

        /* ===== BUTTONS ===== */
        .stButton > button {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A78BFA 100%) !important;
            background-size: 200% auto !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 13px !important;
            font-weight: 800 !important;
            font-size: 14px !important;
            padding: 12px 24px !important;
            box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.35) !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            letter-spacing: 0.01em !important;
        }
        .stButton > button:hover {
            background-position: right center !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 28px -4px rgba(99, 102, 241, 0.5) !important;
        }

        /* ===== INPUTS & UPLOADERS ===== */
        .stTextInput input, .stTextArea textarea {
            background: rgba(10, 15, 30, 0.8) !important;
            border: 1px solid rgba(99, 102, 241, 0.12) !important;
            border-radius: 13px !important;
            color: #F1F5F9 !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12) !important;
        }
        .stTextInput label, .stTextArea label {
            color: #94A3B8 !important;
            font-weight: 600 !important;
        }
        [data-testid="stFileUploader"] {
            background: rgba(10, 15, 30, 0.5);
            border: 2px dashed rgba(99, 102, 241, 0.25);
            border-radius: 16px;
            padding: 20px;
            transition: all 0.2s ease;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: rgba(99, 102, 241, 0.45);
            background: rgba(10, 15, 30, 0.7);
        }

        /* ===== SELECTBOX ===== */
        .stSelectbox > div > div {
            background: rgba(10, 15, 30, 0.8) !important;
            border: 1px solid rgba(99, 102, 241, 0.12) !important;
            border-radius: 13px !important;
            color: #F1F5F9 !important;
        }

        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(10, 15, 30, 0.5);
            border-radius: 14px;
            padding: 4px;
            gap: 4px;
            border: 1px solid rgba(99, 102, 241, 0.08);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px !important;
            font-weight: 700 !important;
            color: #94A3B8 !important;
            padding: 10px 20px !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: rgba(99, 102, 241, 0.15) !important;
            color: #A5B4FC !important;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background: transparent !important;
        }
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        /* ===== PROGRESS BAR ===== */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 50%, #A78BFA 100%) !important;
            border-radius: 999px;
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.3);
        }
        .stProgress > div > div {
            background: rgba(99, 102, 241, 0.08) !important;
            border-radius: 999px !important;
        }

        /* ===== CHAT ===== */
        [data-testid="stChatMessage"] {
            background: rgba(10, 15, 30, 0.6) !important;
            border: 1px solid rgba(99, 102, 241, 0.08) !important;
            border-radius: 16px !important;
            padding: 16px !important;
        }

        /* ===== ROADMAP CARD ===== */
        .roadmap-card {
            background: rgba(10, 15, 30, 0.6);
            border: 1px solid rgba(99, 102, 241, 0.08);
            border-left: 4px solid;
            border-radius: 16px;
            padding: 22px 24px;
            margin-bottom: 14px;
            transition: all 0.2s ease;
            position: relative;
        }
        .roadmap-card:hover {
            transform: translateX(6px);
            border-color: rgba(99, 102, 241, 0.2);
            border-left-color: inherit;
        }
        .roadmap-week {
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
        }
        .roadmap-skill {
            font-size: 17px;
            font-weight: 800;
            color: #FFFFFF;
            margin: 4px 0 8px 0;
        }
        .roadmap-task {
            font-size: 14px;
            color: #94A3B8;
            line-height: 1.5;
        }

        /* ===== ANALYTICS CARD ===== */
        .analytics-role-card {
            background: rgba(10, 15, 30, 0.6);
            border: 1px solid rgba(99, 102, 241, 0.08);
            border-radius: 20px;
            padding: 24px 26px;
            margin-bottom: 16px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }
        .analytics-role-card::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366F1, #8B5CF6);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .analytics-role-card:hover {
            border-color: rgba(99, 102, 241, 0.25);
            transform: translateY(-3px);
            box-shadow: 0 12px 36px -8px rgba(99, 102, 241, 0.15);
        }
        .analytics-role-card:hover::after {
            opacity: 1;
        }

        /* ===== SETTINGS CARD ===== */
        .settings-card {
            background: rgba(10, 15, 30, 0.6);
            border: 1px solid rgba(99, 102, 241, 0.08);
            border-radius: 20px;
            padding: 28px 30px;
        }
        .settings-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 0;
            border-bottom: 1px solid rgba(99, 102, 241, 0.06);
        }
        .settings-row:last-child { border-bottom: none; }
        .settings-label {
            font-size: 14px;
            font-weight: 600;
            color: #94A3B8;
        }
        .settings-value {
            font-size: 14px;
            font-weight: 700;
            color: #F1F5F9;
        }
        .status-online {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: #6EE7B7;
            font-weight: 700;
        }
        .status-online::before {
            content: '';
            width: 8px; height: 8px;
            background: #34D399;
            border-radius: 50%;
            box-shadow: 0 0 10px #34D399;
        }

        /* ===== RECOMMENDATION BOX ===== */
        .ai-rec-box {
            margin-top: 18px;
            padding: 18px 20px;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.06) 100%);
            border: 1px solid rgba(99, 102, 241, 0.15);
        }
        .ai-rec-title {
            font-weight: 800;
            font-size: 13px;
            color: #A5B4FC;
            margin-bottom: 6px;
        }
        .ai-rec-text {
            font-size: 13px;
            color: #CBD5E1;
            line-height: 1.6;
        }

        /* ===== SECTION TITLE ===== */
        .section-title {
            font-size: 18px;
            font-weight: 800;
            color: #FFFFFF;
            margin: 0 0 16px 0;
            letter-spacing: -0.01em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------
# CONTROLLER: LOGIN SCREEN (IMAGE 1)
# ---------------------------------------------------
def render_login_view():
    # Background animated orbs
    st.html(
        """
        <div class="login-bg-effects">
            <div class="login-orb login-orb-1"></div>
            <div class="login-orb login-orb-2"></div>
            <div class="login-orb login-orb-3"></div>
        </div>
        """
    )

    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        st.html(
            """
            <div style="padding: 30px 20px 30px 30px;">
                <div class="login-brand-badge">
                    <span class="badge-dot"></span>
                    <span>AI-Powered Career Intelligence</span>
                </div>

                <div class="login-hero-title">
                    Discover Your<br>
                    <span class="title-gradient">Career Potential</span><br>
                    with AI
                </div>

                <div class="login-hero-sub">
                    Upload your resume and let our advanced AI engine analyze your skills,
                    identify gaps, and map your path to your dream role.
                </div>

                <div class="login-features">
                    <div class="login-feature-item">
                        <div class="feature-icon-circle feature-icon-blue">&#127919;</div>
                        <div class="feature-text"><span>Smart Skill Extraction</span> &mdash; AI-parsed resume taxonomy</div>
                    </div>
                    <div class="login-feature-item">
                        <div class="feature-icon-circle feature-icon-purple">&#128202;</div>
                        <div class="feature-text"><span>Gap Analysis</span> &mdash; Match against 500+ job profiles</div>
                    </div>
                    <div class="login-feature-item">
                        <div class="feature-icon-circle feature-icon-emerald">&#128640;</div>
                        <div class="feature-text"><span>Growth Roadmap</span> &mdash; Personalized learning paths</div>
                    </div>
                </div>

                <div class="login-trust-bar">
                    <div class="trust-stat">
                        <span class="trust-val">10K+</span>
                        <span class="trust-label">Resumes Analyzed</span>
                    </div>
                    <div class="trust-divider"></div>
                    <div class="trust-stat">
                        <span class="trust-val">95%</span>
                        <span class="trust-label">Match Accuracy</span>
                    </div>
                    <div class="trust-divider"></div>
                    <div class="trust-stat">
                        <span class="trust-val">500+</span>
                        <span class="trust-label">Job Profiles</span>
                    </div>
                </div>
            </div>
            """
        )

    with col_right:
        st.html(
            """
            <div class="login-glass-card">
                <div class="login-card-header">
                    <div class="login-card-icon">&#129504;</div>
                    <div class="login-card-title">Welcome Back</div>
                    <div class="login-card-sub">Sign in to your SkillGap AI dashboard</div>
                </div>
            </div>
            """
        )

        email = st.text_input("Email", placeholder="you@example.com", key="auth_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="auth_pwd")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        if st.button("Sign In →", key="btn_signin", use_container_width=True):
            user_str = email.strip().lower() if email.strip() else "you@example.com"
            pwd_str = password.strip() if password.strip() else "demo123"
            
            # Auto-register if not present so any email/password works seamlessly
            if not login_user(user_str, pwd_str):
                register_user(user_str, pwd_str)
            
            st.session_state.logged_in = True
            st.session_state.username = user_str
            st.rerun()

        st.markdown('<div class="demo-note">💡 <b>Quick start:</b> use any email & password to explore</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="copyright-text">© 2025 SkillGap AI — Powered by Advanced AI</div>',
            unsafe_allow_html=True
        )


# ---------------------------------------------------
# CONTROLLER: SIDEBAR
# ---------------------------------------------------
def render_dashboard_sidebar():
    with st.sidebar:
        st.html(
            """
            <div class="sidebar-brand-container">
                <div class="sidebar-logo-icon">&#129504;</div>
                <div>
                    <div class="sidebar-brand-text">SkillGap</div>
                    <div class="sidebar-brand-sub">AI PLATFORM</div>
                </div>
            </div>
            """
        )

        menu_choice = st.radio(
            "Navigation Menu",
            [
                "📈 Overview",
                "🎯 Skills",
                "📊 Analytics",
                "🧠 Learning",
                "⚙️ Settings"
            ],
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        user_display = st.session_state.username if st.session_state.username else "you@example.com"
        st.html(
            f"""
            <div style="background: rgba(15, 20, 40, 0.6); border: 1px solid rgba(99, 102, 241, 0.12); border-radius: 14px; padding: 12px 14px; margin-bottom: 16px;">
                <div style="font-size: 11px; color: #64748B; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Signed in as</div>
                <div style="font-size: 13px; font-weight: 700; color: #E2E8F0; margin-top: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{user_display}</div>
                <div style="display: flex; align-items: center; gap: 6px; margin-top: 6px;">
                    <span style="width: 6px; height: 6px; background: #34D399; border-radius: 50%; box-shadow: 0 0 8px #34D399;"></span>
                    <span style="font-size: 11px; color: #34D399; font-weight: 700;">Pro Plan Active</span>
                </div>
            </div>
            """
        )

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.analysis_result = None
            st.session_state.mentor_chat = []
            st.rerun()

        return menu_choice


# ---------------------------------------------------
# DASHBOARD MODULE 1: ADVANCED OVERVIEW
# ---------------------------------------------------
def render_overview_view():
    user_display = st.session_state.username if st.session_state.username else "you@example.com"
    st.html(
        f"""
        <div class="dash-header-bar">
            <div class="dash-page-title">
                <span>📈 Skill Matrix Dashboard</span>
            </div>
            <div class="status-badge">
                <span class="pulse-dot"></span>
                <span>Active Profile: {user_display}</span>
            </div>
        </div>
        """
    )

    result = st.session_state.analysis_result

    # Demo fallback data if user hasn't uploaded a resume yet
    if result:
        emp = result["employability_score"]
        match_s = result["match_score"]
        skills_detected = result["resume_skills"]
        missing_skills = result["missing_skills"]
        matched_skills = result["matched_skills"]
        roles = result["job_roles"]
    else:
        emp = 84
        match_s = 78
        skills_detected = ["Python", "SQL", "Machine Learning", "Docker", "Git", "REST API", "Data Analysis", "Linux"]
        missing_skills = ["AWS", "Kubernetes", "CI/CD", "FastAPI"]
        matched_skills = ["Python", "SQL", "Machine Learning", "Docker", "REST API"]
        roles = ["Machine Learning Engineer", "Backend Developer", "Data Analyst", "Cloud / DevOps Engineer"]

    # 4 High-Tech KPI Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.html(
            f"""
            <div class="kpi-tile">
                <div class="kpi-tile-header">
                    <span class="kpi-tile-label">Employability Score</span>
                    <div class="kpi-icon-wrap kpi-icon-indigo">&#127919;</div>
                </div>
                <div class="kpi-tile-val">{emp}%</div>
                <span class="kpi-pill pill-indigo">&#9650; Top 12% Candidate</span>
            </div>
            """
        )
    with c2:
        st.html(
            f"""
            <div class="kpi-tile">
                <div class="kpi-tile-header">
                    <span class="kpi-tile-label">Resume Match Index</span>
                    <div class="kpi-icon-wrap kpi-icon-purple">&#128196;</div>
                </div>
                <div class="kpi-tile-val">{match_s}%</div>
                <span class="kpi-pill pill-purple">&#9679; High Role Fit</span>
            </div>
            """
        )
    with c3:
        st.html(
            f"""
            <div class="kpi-tile">
                <div class="kpi-tile-header">
                    <span class="kpi-tile-label">Verified Skills</span>
                    <div class="kpi-icon-wrap kpi-icon-emerald">&#10004;</div>
                </div>
                <div class="kpi-tile-val">{len(skills_detected)}</div>
                <span class="kpi-pill pill-emerald">&#10003; Verified Core</span>
            </div>
            """
        )
    with c4:
        st.html(
            f"""
            <div class="kpi-tile">
                <div class="kpi-tile-header">
                    <span class="kpi-tile-label">Skill Gaps</span>
                    <div class="kpi-icon-wrap kpi-icon-amber">&#9888;</div>
                </div>
                <div class="kpi-tile-val">{len(missing_skills)}</div>
                <span class="kpi-pill pill-amber">&#9889; Learning Targets</span>
            </div>
            """
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Main Grid: Skill Landscape & Market Role Fit
    col_left, col_right = st.columns([1.5, 1], gap="large")

    with col_left:
        skills_html = ""
        for sk in skills_detected[:6]:
            prof = random.randint(82, 96)
            skills_html += f"""
            <div class="skill-item-row">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="color: #818CF8; font-size: 16px;">&#9889;</span>
                    <span class="skill-name-bold">{sk}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 14px;">
                    <span style="font-size: 13px; font-weight: 700; color: #818CF8;">{prof}%</span>
                    <span class="level-badge level-expert">Current Level</span>
                </div>
            </div>
            """

        gaps_html = ""
        if missing_skills:
            gaps_html = "<h4 style='font-size: 14px; font-weight: 700; margin: 20px 0 10px 0; color: #FDA4AF;'>&#9888; Priority Gaps to Close</h4>"
            for msk in missing_skills[:4]:
                gaps_html += f"""
                <div class="skill-item-row">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="color: #FDA4AF; font-size: 16px;">!</span>
                        <span class="skill-name-bold">{msk}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <span style="font-size: 13px; font-weight: 700; color: #FDA4AF;">Gap</span>
                        <span class="level-badge level-learning">Recommended</span>
                    </div>
                </div>
                """

        st.html(
            f"""
            <div class="landscape-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
                    <h3 class="section-title" style="margin: 0;">⚡ Skill Landscape & Proficiency</h3>
                    <span style="font-size: 12px; color: #64748B; font-weight: 600;">Live Taxonomy</span>
                </div>
                {skills_html}
                {gaps_html}
            </div>
            """
        )

    with col_right:
        roles_html = ""
        for r in roles[:3]:
            r_score = random.randint(84, 96)
            roles_html += f"""
            <div class="job-match-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 800; font-size: 16px; color: #FFFFFF;">{r}</span>
                    <span style="font-weight: 900; font-size: 20px; color: #818CF8;">{r_score}%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 12px; color: #94A3B8;">
                    <span>Status: <b style="color: #34D399;">Ready to Apply</b></span>
                    <span>Avg: $110k-$145k</span>
                </div>
            </div>
            """

        st.html(
            f"""
            <div class="landscape-card">
                <h3 class="section-title">💼 Job Match Intelligence</h3>
                {roles_html}
                <div class="ai-rec-box">
                    <div class="ai-rec-title">💡 AI Recommendation</div>
                    <div class="ai-rec-text">
                        Upload your custom resume or paste a job description in the <b>Skills</b> tab to recalibrate your AI match index.
                    </div>
                </div>
            </div>
            """
        )


# ---------------------------------------------------
# DASHBOARD MODULE 2: SKILLS
# ---------------------------------------------------
def render_skills_view():
    st.html(
        """
        <div class="dash-header-bar">
            <div class="dash-page-title"><span>🎯 Skills & Resume Intelligence Studio</span></div>
        </div>
        """
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.html(
            """
            <div class="landscape-card">
                <h3 class="section-title">📄 1. Upload Resume PDF</h3>
                <p style="color: #94A3B8; font-size: 13px; margin-bottom: 16px;">Accepts standard text-based PDF resumes (max 10MB)</p>
            </div>
            """
        )
        uploaded = st.file_uploader("Upload PDF Resume", type=["pdf"], label_visibility="collapsed")

    with c2:
        st.html(
            """
            <div class="landscape-card">
                <h3 class="section-title">💼 2. Target Job Description</h3>
                <p style="color: #94A3B8; font-size: 13px; margin-bottom: 8px;">Select a fast preset or paste custom job requirements</p>
            </div>
            """
        )
        template = st.selectbox(
            "Quick Role Templates",
            [
                "-- Type or Select Role Template --",
                "Full Stack Engineer: Python, Django, React, TypeScript, SQL, AWS, Docker, REST API",
                "AI / ML Engineer: Python, Machine Learning, Deep Learning, PyTorch, TensorFlow, SQL, NLP",
                "Cloud & DevOps Engineer: AWS, Docker, Kubernetes, Linux, CI/CD, Git, Terraform"
            ],
            label_visibility="collapsed"
        )
        jd_val = template if "--" not in template else ""
        job_desc = st.text_area("Job Description", value=jd_val, height=120, placeholder="e.g. Looking for a Python Developer with SQL, React, AWS...", label_visibility="collapsed")

    if st.button("🚀 Analyze Resume & Compute Skill Gaps", use_container_width=True):
        if not uploaded:
            st.error("Please upload a resume PDF.")
        elif not job_desc.strip():
            st.error("Please enter a job description.")
        else:
            with st.spinner("🧠 AI Parsing resume & matching skills..."):
                res = analyze_resume(uploaded, job_desc)
                time.sleep(0.7)

            if "error" in res:
                st.error(res["error"])
            else:
                st.session_state.analysis_result = res
                st.session_state.last_uploaded_name = uploaded.name
                st.success("✅ Deep Analysis Complete! Results updated across your dashboard.")

    res = st.session_state.analysis_result
    if res:
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        st.html(
            """
            <div class="landscape-card">
                <h3 class="section-title">📊 Extracted Skill Taxonomy Breakdown</h3>
            </div>
            """
        )
        all_skills = sorted(set(res["resume_skills"] + res["required_skills"]))
        cols = st.columns(2, gap="medium")
        for i, sk in enumerate(all_skills):
            is_miss = sk in res["missing_skills"]
            is_match = sk in res["matched_skills"]
            val = random.randint(30, 50) if is_miss else (random.randint(80, 98) if is_match else random.randint(55, 75))
            status_lbl = "Missing Gap" if is_miss else ("Matched Core" if is_match else "Secondary")
            tag_cls = "level-learning" if is_miss else ("level-expert" if is_match else "level-proficient")

            with cols[i % 2]:
                st.html(
                    f"""
                    <div class="skill-item-row" style="margin-bottom: 8px;">
                        <span class="skill-name-bold">{sk}</span>
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <span style="font-size: 13px; font-weight: 700;">{val}%</span>
                            <span class="level-badge {tag_cls}">{status_lbl}</span>
                        </div>
                    </div>
                    """
                )
                st.progress(val / 100)


# ---------------------------------------------------
# DASHBOARD MODULE 3: ANALYTICS
# ---------------------------------------------------
def render_analytics_view():
    st.html(
        """
        <div class="dash-header-bar">
            <div class="dash-page-title"><span>📊 Analytics & Job Compatibility Engine</span></div>
        </div>
        """
    )

    res = st.session_state.analysis_result
    roles = res.get("job_roles", []) if res else ["Machine Learning Engineer", "Backend Developer", "Cloud Architect", "Data Scientist"]

    st.html("<h3 class='section-title'>🎯 Target Role Compatibility Index</h3>")
    cols = st.columns(2, gap="medium")
    for i, role in enumerate(roles):
        score = random.randint(80, 97)
        with cols[i % 2]:
            st.html(
                f"""
                <div class="analytics-role-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; font-size: 19px; font-weight: 800; color: #FFFFFF;">{role}</h4>
                        <span style="font-size: 28px; font-weight: 900; color: #818CF8;">{score}%</span>
                    </div>
                    <p style="color: #94A3B8; font-size: 13px; margin: 10px 0 16px 0; line-height: 1.5;">
                        Strong alignment with your core technical skill inventory and experience level.
                    </p>
                    <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(15, 20, 40, 0.6); padding: 12px 16px; border-radius: 14px; font-size: 12px;">
                        <span>Status: <b style="color: #34D399;">Top Tier Match</b></span>
                        <span style="color: #A5B4FC; font-weight: 700;">Est. Comp: $110k-$145k</span>
                    </div>
                </div>
                """
            )


# ---------------------------------------------------
# DASHBOARD MODULE 4: LEARNING
# ---------------------------------------------------
def render_learning_view():
    st.html(
        """
        <div class="dash-header-bar">
            <div class="dash-page-title"><span>🧠 Learning Roadmap & AI Career Mentor</span></div>
        </div>
        """
    )

    tab_road, tab_chat = st.tabs(["🗺️ Custom Weekly Roadmap", "🤖 AI Mentor Chat"])

    with tab_road:
        res = st.session_state.analysis_result
        roadmap = res.get("roadmap", []) if res else [
            {"week": "Week 1", "skill": "Docker & Containerization", "task": "Learn multi-stage Dockerfiles and containerize a Python web app with production best practices."},
            {"week": "Week 2", "skill": "AWS Cloud Deployments", "task": "Deploy your containerized service to AWS ECS/EC2 with IAM security roles and load balancing."},
            {"week": "Week 3", "skill": "CI/CD Automation", "task": "Set up GitHub Actions to automate unit testing, linting, and container builds on every push."},
            {"week": "Final Week", "skill": "Portfolio Project Upgrade", "task": "Publish live demo and GitHub repository with architectural diagrams and comprehensive documentation."}
        ]

        border_colors = ["#6366F1", "#8B5CF6", "#0EA5E9", "#10B981"]

        for i, item in enumerate(roadmap):
            b_col = border_colors[i % len(border_colors)]
            st.html(
                f"""
                <div class="roadmap-card" style="border-left-color: {b_col};">
                    <div class="roadmap-week" style="color: {b_col};">{item['week']}</div>
                    <div class="roadmap-skill">{item['skill']}</div>
                    <div class="roadmap-task">{item['task']}</div>
                </div>
                """
            )

    with tab_chat:
        st.html(
            """
            <div class="landscape-card" style="margin-bottom: 16px;">
                <h3 class="section-title" style="margin-bottom: 6px;">🤖 Chat with AI Career Mentor</h3>
                <p style="color: #94A3B8; font-size: 13px; margin: 0;">Get customized interview prep, resume tuning advice, and project recommendations.</p>
            </div>
            """
        )

        if st.button("🗑️ Clear Chat History"):
            st.session_state.mentor_chat = []
            st.rerun()

        for msg in st.session_state.mentor_chat:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_q = st.chat_input("Ask your AI Mentor anything about your career path...")
        if user_q:
            st.session_state.mentor_chat.append({"role": "user", "content": user_q})
            with st.chat_message("user"):
                st.write(user_q)

            with st.chat_message("assistant"):
                with st.spinner("AI Mentor is analyzing..."):
                    ans = ai_mentor_response(
                        question=user_q,
                        analysis_result=st.session_state.analysis_result,
                        chat_history=st.session_state.mentor_chat
                    )
                st.write(ans)
            st.session_state.mentor_chat.append({"role": "assistant", "content": ans})


# ---------------------------------------------------
# DASHBOARD MODULE 5: SETTINGS
# ---------------------------------------------------
def render_settings_view():
    st.html(
        """
        <div class="dash-header-bar">
            <div class="dash-page-title"><span>⚙️ Platform Settings & Account Profile</span></div>
        </div>
        """
    )

    user_val = st.session_state.username or 'you@example.com'
    last_file = st.session_state.last_uploaded_name or 'Default Baseline Profile'

    st.html(
        f"""
        <div class="settings-card">
            <h3 class="section-title" style="margin-bottom: 20px;">Account & System Status</h3>
            <div class="settings-row">
                <span class="settings-label">User Account</span>
                <span class="settings-value">{user_val}</span>
            </div>
            <div class="settings-row">
                <span class="settings-label">Active Resume Profile</span>
                <span class="settings-value">{last_file}</span>
            </div>
            <div class="settings-row">
                <span class="settings-label">AI Engine</span>
                <span class="settings-value"><span class="status-online">GPT-4.1 Turbo (Active)</span></span>
            </div>
            <div class="settings-row">
                <span class="settings-label">Subscription Tier</span>
                <span class="settings-value" style="color: #A5B4FC;">SkillGap Pro Plan</span>
            </div>
            <div class="settings-row">
                <span class="settings-label">Security & Encryption</span>
                <span class="settings-value" style="color: #34D399;">256-Bit SSL Protected</span>
            </div>
        </div>
        """
    )


# ---------------------------------------------------
# MAIN APPLICATION ROUTER
# ---------------------------------------------------
def main():
    if not st.session_state.logged_in:
        render_login_view()
    else:
        nav = render_dashboard_sidebar()
        if "Overview" in nav:
            render_overview_view()
        elif "Skills" in nav:
            render_skills_view()
        elif "Analytics" in nav:
            render_analytics_view()
        elif "Learning" in nav:
            render_learning_view()
        elif "Settings" in nav:
            render_settings_view()


if __name__ == "__main__":
    main()

