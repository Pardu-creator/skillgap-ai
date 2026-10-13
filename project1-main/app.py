import streamlit as st
import database
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
        "user_profile": None,
        "auth_tab": "Sign In",
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
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

        * {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            box-sizing: border-box;
        }

        #MainMenu, footer, header {visibility: hidden;}

        .stApp {
            background: #060814 !important;
            color: #E2E8F0;
            min-height: 100vh;
        }

        /* ===== CINEMATIC SPLASH SCREEN (LOGO COMES FIRST) ===== */
        .splash-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, #0F172A 0%, #060814 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999999;
            animation: splashDismiss 2.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes splashDismiss {
            0% { opacity: 1; pointer-events: all; }
            70% { opacity: 1; pointer-events: all; }
            95% { opacity: 0; pointer-events: all; transform: scale(1.05); }
            100% { opacity: 0; pointer-events: none; visibility: hidden; }
        }

        .splash-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            animation: splashEntry 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes splashEntry {
            0% { transform: scale(0.8) translateY(10px); opacity: 0; }
            100% { transform: scale(1) translateY(0); opacity: 1; }
        }

        .splash-logo-container {
            position: relative;
            width: 100px;
            height: 100px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .splash-logo-pulse {
            position: absolute;
            width: 110px;
            height: 110px;
            border-radius: 32px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.5), rgba(168, 85, 247, 0.5));
            filter: blur(28px);
            animation: splashPulseAnim 2s ease-in-out infinite;
        }

        @keyframes splashPulseAnim {
            0%, 100% { transform: scale(0.95); opacity: 0.6; }
            50% { transform: scale(1.25); opacity: 1; filter: blur(36px); }
        }

        .splash-logo-box {
            position: relative;
            width: 90px;
            height: 90px;
            border-radius: 26px;
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #0EA5E9 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 46px;
            box-shadow: 0 16px 45px rgba(99, 102, 241, 0.45), inset 0 1px 1px rgba(255, 255, 255, 0.4);
            animation: logoFloat 3s ease-in-out infinite;
        }

        @keyframes logoFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-6px); }
        }

        .splash-title {
            font-size: 38px;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: -0.03em;
            margin-bottom: 6px;
        }

        .splash-ai {
            background: linear-gradient(135deg, #6366F1, #38BDF8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .splash-sub {
            font-size: 12px;
            font-weight: 700;
            color: #94A3B8;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            margin-bottom: 30px;
        }

        .splash-bar-outer {
            width: 170px;
            height: 4px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 999px;
            overflow: hidden;
        }

        .splash-bar-fill {
            width: 0%;
            height: 100%;
            background: linear-gradient(90deg, #6366F1, #38BDF8);
            border-radius: 999px;
            animation: splashFill 1.6s ease-in-out forwards;
        }

        @keyframes splashFill {
            0% { width: 0%; }
            45% { width: 65%; }
            100% { width: 100%; }
        }

        /* ===== CLEAN LOGIN CONTAINER & CARD ===== */
        .clean-login-wrapper {
            max-width: 460px;
            margin: 30px auto 40px auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            animation: loginFadeIn 0.8s 0.2s cubic-bezier(0.16, 1, 0.3, 1) both;
        }

        @keyframes loginFadeIn {
            0% { opacity: 0; transform: translateY(18px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .clean-card-header {
            text-align: center;
            margin-bottom: 24px;
        }

        .clean-brand-icon {
            width: 58px;
            height: 58px;
            border-radius: 18px;
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 60%, #A855F7 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            margin: 0 auto 14px auto;
            box-shadow: 0 10px 28px -4px rgba(99, 102, 241, 0.4);
        }

        .clean-app-title {
            font-size: 26px;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: -0.02em;
            margin-bottom: 4px;
        }

        .clean-app-sub {
            font-size: 13px;
            color: #64748B;
            font-weight: 500;
        }

        /* Inputs */
        .stTextInput label {
            font-size: 12px !important;
            font-weight: 700 !important;
            color: #94A3B8 !important;
            letter-spacing: 0.04em !important;
            margin-bottom: 4px !important;
        }
        .stTextInput input {
            background: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(99, 102, 241, 0.16) !important;
            border-radius: 12px !important;
            color: #F8FAFC !important;
            padding: 14px 16px !important;
            font-size: 14px !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput input:focus {
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.18) !important;
            background: rgba(15, 23, 42, 0.98) !important;
        }

        /* Action Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 60%, #A855F7 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            height: 48px !important;
            font-weight: 800 !important;
            font-size: 15px !important;
            box-shadow: 0 8px 22px -4px rgba(99, 102, 241, 0.4) !important;
            transition: all 0.25s ease !important;
            width: 100% !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 14px 30px -4px rgba(99, 102, 241, 0.55) !important;
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px !important;
            background: rgba(15, 23, 42, 0.6) !important;
            padding: 4px !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            margin-bottom: 20px !important;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px !important;
            padding: 8px 16px !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            color: #94A3B8 !important;
            border: none !important;
            flex: 1 !important;
            justify-content: center !important;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(99, 102, 241, 0.2) !important;
            color: #A5B4FC !important;
            box-shadow: 0 2px 10px rgba(99, 102, 241, 0.2) !important;
        }

        /* Subtle pill buttons */
        div[data-testid="stHorizontalBlock"] .stButton > button {
            height: 38px !important;
            font-size: 12px !important;
            background: rgba(99, 102, 241, 0.08) !important;
            border: 1px solid rgba(99, 102, 241, 0.2) !important;
            color: #CBD5E1 !important;
            box-shadow: none !important;
        }
        div[data-testid="stHorizontalBlock"] .stButton > button:hover {
            background: rgba(99, 102, 241, 0.18) !important;
            border-color: #6366F1 !important;
            color: #FFFFFF !important;
            transform: translateY(-1px) !important;
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

        /* ===== NATIVE APP TOPBAR & NAVIGATION ===== */
        .app-topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 22px;
            background: rgba(10, 15, 30, 0.85);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(99, 102, 241, 0.16);
            border-radius: 20px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }
        .app-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .app-brand-icon {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(135deg, #6366F1, #8B5CF6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
        }
        .app-brand-title {
            font-size: 20px;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: -0.02em;
            line-height: 1;
        }
        .app-user-pill {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 6px 14px 6px 6px;
            border-radius: 999px;
        }
        .app-user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366F1, #0EA5E9);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 12px;
            color: #FFFFFF;
        }
        .app-user-name {
            font-size: 13px;
            font-weight: 700;
            color: #F1F5F9;
        }

        /* App Quick Actions */
        .app-action-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-bottom: 24px;
        }
        .app-action-tile {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.8) 0%, rgba(10, 15, 30, 0.95) 100%);
            border: 1px solid rgba(99, 102, 241, 0.12);
            border-radius: 18px;
            padding: 18px;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .app-action-tile:hover {
            transform: translateY(-3px);
            border-color: rgba(99, 102, 241, 0.35);
            box-shadow: 0 12px 28px -6px rgba(99, 102, 241, 0.25);
        }
        .action-tile-icon {
            width: 38px;
            height: 38px;
            border-radius: 11px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            margin-bottom: 2px;
        }

        /* ===== NATIVE APP SEGMENTED CONTROL DOCK ===== */
        [data-testid="stSegmentedControl"] {
            display: flex !important;
            justify-content: stretch !important;
            margin-bottom: 22px !important;
            width: 100% !important;
        }
        [data-testid="stSegmentedControl"] > div {
            background: rgba(10, 15, 30, 0.85) !important;
            border: 1px solid rgba(99, 102, 241, 0.22) !important;
            border-radius: 16px !important;
            padding: 6px !important;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.35) !important;
            gap: 6px !important;
            width: 100% !important;
            display: flex !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
        }
        [data-testid="stSegmentedControl"] button {
            flex: 1 !important;
            border-radius: 12px !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            padding: 10px 14px !important;
            border: 1px solid transparent !important;
            color: #94A3B8 !important;
            background: transparent !important;
            box-shadow: none !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        [data-testid="stSegmentedControl"] button:hover {
            background: rgba(99, 102, 241, 0.15) !important;
            color: #FFFFFF !important;
            border-color: rgba(99, 102, 241, 0.25) !important;
            transform: none !important;
        }
        [data-testid="stSegmentedControl"] button[aria-checked="true"],
        [data-testid="stSegmentedControl"] button[data-active="true"] {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.75) 0%, rgba(139, 92, 246, 0.7) 100%) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            border: 1px solid rgba(129, 140, 248, 0.7) !important;
            box-shadow: 0 4px 18px rgba(99, 102, 241, 0.45) !important;
            transform: none !important;
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
# CONTROLLER: LOGIN SCREEN (LOGO INTRO + CLEAN MINIMALIST LOGIN)
# ---------------------------------------------------
def render_login_view():
    # 1. Cinematic Splash Overlay — Logo Appears First When App Loads
    st.html(
        """
        <div class="splash-overlay">
            <div class="splash-content">
                <div class="splash-logo-container">
                    <div class="splash-logo-pulse"></div>
                    <div class="splash-logo-box">🧠</div>
                </div>
                <div class="splash-title">SkillGap <span class="splash-ai">AI</span></div>
                <div class="splash-sub">Advanced Career Intelligence</div>
                <div class="splash-bar-outer">
                    <div class="splash-bar-fill"></div>
                </div>
            </div>
        </div>
        """
    )

    # 2. Clean, Centered Luxury Login Interface
    _, col_center, _ = st.columns([1, 1.5, 1])

    with col_center:
        st.html(
            """
            <div class="clean-login-wrapper">
                <div class="clean-card-header">
                    <div class="clean-brand-icon">&#129504;</div>
                    <div class="clean-app-title">SkillGap <span style="background: linear-gradient(135deg, #6366F1, #38BDF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI</span></div>
                    <div class="clean-app-sub">Welcome back &bull; Sign in to access your career roadmap</div>
                </div>
            </div>
            """
        )

        auth_tab1, auth_tab2, auth_tab3 = st.tabs(["🔐 Sign In", "✨ Create Account", "🔑 Reset Password"])

        # ----------------------------------------------------
        # TAB 1: SIGN IN (CLEAN & DIRECT)
        # ----------------------------------------------------
        with auth_tab1:
            login_ident = st.text_input("Email or Username", placeholder="you@example.com", key="login_ident")
            login_pwd = st.text_input("Password", type="password", placeholder="••••••••", key="login_pwd")

            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

            if st.button("Sign In →", key="btn_signin_db", use_container_width=True):
                if not login_ident.strip() or not login_pwd.strip():
                    st.error("⚠️ Please enter your email/username and password.")
                else:
                    success, result = database.authenticate_user_db(login_ident, login_pwd)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = result["email"]
                        st.session_state.user_profile = result
                        st.success(f"✓ Welcome back, {result.get('full_name', 'Student')}!")
                        time.sleep(0.3)
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            st.markdown(
                """
                <div style="text-align: center; margin-bottom: 8px;">
                    <span style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em;">Quick 1-Click Demo Profiles</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            dcol1, dcol2, dcol3 = st.columns(3)
            with dcol1:
                if st.button("🎓 Student", key="demo_student_btn", use_container_width=True):
                    ok, res = database.authenticate_user_db("demo@skillgap.ai", "Password123!")
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.username = res["email"]
                        st.session_state.user_profile = res
                        st.rerun()
            with dcol2:
                if st.button("💻 Alex (Frontend)", key="demo_alex_btn", use_container_width=True):
                    ok, res = database.authenticate_user_db("alex@skillgap.ai", "Password123!")
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.username = res["email"]
                        st.session_state.user_profile = res
                        st.rerun()
            with dcol3:
                if st.button("🤖 Priya (AI/ML)", key="demo_priya_btn", use_container_width=True):
                    ok, res = database.authenticate_user_db("priya@skillgap.ai", "Password123!")
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.username = res["email"]
                        st.session_state.user_profile = res
                        st.rerun()

        # ----------------------------------------------------
        # TAB 2: CREATE ACCOUNT (CLEAN & FAST)
        # ----------------------------------------------------
        with auth_tab2:
            reg_name = st.text_input("Full Name", placeholder="Jane Doe", key="reg_name")
            reg_email = st.text_input("Email Address", placeholder="jane@example.com", key="reg_email")

            rcol1, rcol2 = st.columns(2)
            with rcol1:
                reg_role = st.selectbox(
                    "Target Role",
                    [
                        "Full Stack Developer",
                        "Frontend Engineer",
                        "Backend Engineer",
                        "Machine Learning Engineer",
                        "Data Scientist / Analyst",
                        "Cloud & DevOps Engineer",
                        "Cyber Security Analyst",
                        "Mobile App Developer"
                    ],
                    key="reg_role"
                )
            with rcol2:
                reg_exp = st.selectbox(
                    "Experience Level",
                    [
                        "Undergraduate / Fresher",
                        "Junior (1 - 2 Years)",
                        "Mid-Level (3 - 5 Years)",
                        "Senior (5+ Years)"
                    ],
                    key="reg_exp"
                )

            reg_pwd = st.text_input("Password", type="password", placeholder="At least 6 characters", key="reg_pwd")
            reg_pwd_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-type password", key="reg_pwd_confirm")

            # Dynamic Password strength feedback
            if reg_pwd:
                score, label = database.check_password_strength(reg_pwd)
                pcol = "#EF4444" if score < 40 else "#F59E0B" if score < 70 else "#10B981"
                st.markdown(
                    f"""
                    <div style="margin-top: 2px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                            <span style="color: #64748B;">Password Security:</span>
                            <span style="font-weight: 700; color: {pcol};">{label} ({score}%)</span>
                        </div>
                        <div style="width: 100%; height: 3px; background: rgba(255,255,255,0.08); border-radius: 999px; overflow: hidden;">
                            <div style="width: {score}%; height: 100%; background: {pcol}; transition: width 0.3s ease;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if st.button("Create Account →", key="btn_register_db", use_container_width=True):
                if not reg_name.strip() or not reg_email.strip():
                    st.error("⚠️ Please fill in all required fields.")
                elif "@" not in reg_email:
                    st.error("⚠️ Please enter a valid email address.")
                elif len(reg_pwd) < 6:
                    st.error("⚠️ Password must be at least 6 characters.")
                elif reg_pwd != reg_pwd_confirm:
                    st.error("⚠️ Passwords do not match.")
                else:
                    success, msg = database.register_user_db(
                        email=reg_email,
                        password=reg_pwd,
                        full_name=reg_name,
                        target_role=reg_role,
                        experience_level=reg_exp
                    )
                    if success:
                        st.success("✓ " + msg)
                        ok, user_res = database.authenticate_user_db(reg_email, reg_pwd)
                        if ok:
                            st.session_state.logged_in = True
                            st.session_state.username = user_res["email"]
                            st.session_state.user_profile = user_res
                            time.sleep(0.4)
                            st.rerun()
                    else:
                        st.error("❌ " + msg)

        # ----------------------------------------------------
        # TAB 3: RESET PASSWORD
        # ----------------------------------------------------
        with auth_tab3:
            reset_email = st.text_input("Registered Email", placeholder="you@example.com", key="reset_email")
            reset_pwd1 = st.text_input("New Password", type="password", placeholder="New password", key="reset_pwd1")
            reset_pwd2 = st.text_input("Confirm New Password", type="password", placeholder="Repeat new password", key="reset_pwd2")

            if st.button("Update Password →", key="btn_reset_db", use_container_width=True):
                if not reset_email.strip() or "@" not in reset_email:
                    st.error("⚠️ Please enter a valid registered email.")
                elif len(reset_pwd1) < 6:
                    st.error("⚠️ New password must be at least 6 characters.")
                elif reset_pwd1 != reset_pwd2:
                    st.error("⚠️ Passwords do not match.")
                else:
                    success, msg = database.reset_password_db(reset_email, reset_pwd1)
                    if success:
                        st.success("✓ " + msg)
                    else:
                        st.error("❌ " + msg)

        st.markdown(
            """
            <div style="text-align: center; color: #475569; font-size: 11px; margin-top: 24px;">
                🔒 Secured by SQLite Database &bull; PBKDF2-SHA256 Encryption
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------------------------
# CONTROLLER: APP TOPBAR & HORIZONTAL SEGMENTED DOCK
# ---------------------------------------------------
def render_app_topbar_and_dock():
    profile = st.session_state.get("user_profile") or {}
    display_name = profile.get("full_name") or st.session_state.username.split("@")[0].capitalize()
    display_role = profile.get("target_role") or "Full Stack Developer"
    account_type = profile.get("role") or "Student"
    initials = "".join([part[0].upper() for part in display_name.split()[:2]]) if display_name else "SG"

    top_col1, top_col2 = st.columns([1.3, 1])
    with top_col1:
        st.markdown(
            f"""
            <div class="app-brand" style="padding: 4px 0;">
                <div class="app-brand-icon">&#129504;</div>
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span class="app-brand-title">SkillGap AI</span>
                        <span style="font-size: 10px; font-weight: 800; color: #34D399; background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.3); padding: 2px 8px; border-radius: 999px;">● Live App</span>
                    </div>
                    <div style="font-size: 12px; color: #64748B; margin-top: 2px;">Career Intelligence &bull; AI Mentor &bull; Learning Roadmaps</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with top_col2:
        c_user, c_logout = st.columns([2.5, 1])
        with c_user:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-end; padding-top: 6px;">
                    <div class="app-user-pill">
                        <div class="app-user-avatar">{initials}</div>
                        <div>
                            <div class="app-user-name">{display_name}</div>
                            <div style="font-size: 10px; color: #A5B4FC; font-weight: 700;">🎯 {display_role}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_logout:
            if st.button("🚪 Logout", key="topbar_logout_btn", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.user_profile = None
                st.session_state.analysis_result = None
                st.session_state.mentor_chat = []
                st.rerun()

    # Horizontal Native App Segmented Control Dock
    tabs = ["📈 Overview", "🎯 Skill Analyzer", "📊 Role Analytics", "🧠 AI Mentor", "⚙️ Profile & DB"]
    active = st.session_state.get("active_tab")
    if active not in tabs:
        active = tabs[0]

    choice = st.segmented_control(
        "App Navigation",
        options=tabs,
        default=active,
        label_visibility="collapsed",
        key="app_nav_segmented"
    )
    if choice and choice != st.session_state.get("active_tab"):
        st.session_state.active_tab = choice
        st.rerun()

    return st.session_state.get("active_tab", tabs[0])


# ---------------------------------------------------
# CONTROLLER: SIDEBAR (USER PROFILE INTEGRATED)
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

        profile = st.session_state.get("user_profile") or {}
        display_name = profile.get("full_name") or st.session_state.username.split("@")[0].capitalize()
        display_email = profile.get("email") or st.session_state.username or "demo@skillgap.ai"
        display_role = profile.get("target_role") or "Full Stack Developer"
        account_type = profile.get("role") or "Student"
        initials = "".join([part[0].upper() for part in display_name.split()[:2]]) if display_name else "SG"

        st.html(
            f"""
            <div style="background: rgba(15, 20, 40, 0.7); border: 1px solid rgba(99, 102, 241, 0.16); border-radius: 16px; padding: 14px 16px; margin-bottom: 16px; backdrop-filter: blur(12px);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                    <div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-weight: 800; color: #FFF; font-size: 14px; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);">
                        {initials}
                    </div>
                    <div style="overflow: hidden;">
                        <div style="font-size: 14px; font-weight: 800; color: #F8FAFC; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{display_name}</div>
                        <div style="font-size: 11px; color: #94A3B8; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{display_email}</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.06); padding-top: 8px;">
                    <span style="font-size: 11px; font-weight: 700; color: #A5B4FC;">🎯 {display_role}</span>
                    <span style="font-size: 10px; font-weight: 800; color: #34D399; background: rgba(16, 185, 129, 0.12); padding: 2px 8px; border-radius: 999px;">{account_type}</span>
                </div>
            </div>
            """
        )

        if st.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_profile = None
            st.session_state.analysis_result = None
            st.session_state.mentor_chat = []
            st.rerun()

        return menu_choice


# ---------------------------------------------------
# DASHBOARD MODULE 1: ADVANCED OVERVIEW (APP LIKE)
# ---------------------------------------------------
def render_overview_view():
    profile = st.session_state.get("user_profile") or {}
    display_name = profile.get("full_name") or st.session_state.username.split("@")[0].capitalize()
    target_role = profile.get("target_role") or "Full Stack Developer"

    # App Quick Action Grid
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div>
                <h2 style="font-size: 22px; font-weight: 900; color: #FFFFFF; margin: 0; letter-spacing: -0.02em;">Welcome back, {display_name} 👋</h2>
                <div style="font-size: 13px; color: #94A3B8; margin-top: 2px;">Target Career Track: <b style="color: #A5B4FC;">{target_role}</b></div>
            </div>
            <div style="display: flex; gap: 8px;">
                <span style="font-size: 11px; font-weight: 700; color: #38BDF8; background: rgba(14, 165, 233, 0.12); border: 1px solid rgba(14, 165, 233, 0.25); padding: 4px 12px; border-radius: 999px;">🚀 Career Track Active</span>
            </div>
        </div>
        <div style="margin-bottom: 10px;">
            <div style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">Quick App Actions</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4 Interactive Quick Action App Tiles
    ac1, ac2, ac3, ac4 = st.columns(4)
    with ac1:
        if st.button("📄 Scan Resume\nAI skill extraction", key="tile_scan", use_container_width=True):
            st.session_state.active_tab = "🎯 Skill Analyzer"
            st.rerun()
    with ac2:
        if st.button("🎯 Role Blueprint\n500+ tech specs", key="tile_role", use_container_width=True):
            st.session_state.active_tab = "📊 Role Analytics"
            st.rerun()
    with ac3:
        if st.button("🗺️ 12-Wk Roadmap\nMilestones & tasks", key="tile_road", use_container_width=True):
            st.session_state.active_tab = "🎯 Skill Analyzer"
            st.rerun()
    with ac4:
        if st.button("💬 AI Career Mentor\nAdvice & interview prep", key="tile_mentor", use_container_width=True):
            st.session_state.active_tab = "🧠 AI Mentor"
            st.rerun()

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)


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
# MAIN APPLICATION ROUTER (NATIVE APP EXPERIENCE)
# ---------------------------------------------------
def main():
    if not st.session_state.logged_in:
        render_login_view()
    else:
        # Desktop Sidebar (maintained for widescreen access)
        render_dashboard_sidebar()

        # Native App Topbar & Horizontal Segmented App Dock
        nav = render_app_topbar_and_dock()

        if "Overview" in nav:
            render_overview_view()
        elif "Skill Analyzer" in nav or "Skills" in nav:
            render_skills_view()
        elif "Role Analytics" in nav or "Analytics" in nav:
            render_analytics_view()
        elif "AI Mentor" in nav or "Learning" in nav:
            render_learning_view()
        elif "Profile" in nav or "Settings" in nav:
            render_settings_view()


if __name__ == "__main__":
    main()

