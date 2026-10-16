"""Tema visual — Professional Cybersecurity Command Center."""

from __future__ import annotations

import streamlit as st

CORES = {
    "bg": "#06111F",
    "panel": "#081A2B",
    "panel_alt": "#0B2034",
    "border": "#173B58",
    "cyan": "#00D9FF",
    "green": "#00E6A0",
    "purple": "#9B5CFF",
    "red": "#FF365D",
    "orange": "#FF9B35",
    "text": "#F1F6FC",
    "text_muted": "#9CB4CC",
    "slate": "#5A7A99",
    # aliases usados nos gráficos
    "teal": "#00D9FF",
    "blue": "#00D9FF",
    "amber": "#FF9B35",
}


def injetar_css() -> None:
    c = CORES
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', system-ui, sans-serif;
        }}

        header[data-testid="stHeader"] {{
            background: transparent;
            visibility: hidden;
            height: 0 !important;
        }}

        .stApp {{
            background-color: {c["bg"]};
            color: {c["text"]};
        }}

        .block-container {{
            padding-top: 4.5rem !important;
            padding-bottom: 5rem !important;
            max-width: 96rem;
        }}

        [data-testid="stSidebar"] {{
            background: {c["panel"]};
            border-right: 1px solid {c["border"]};
            padding-top: 4.25rem;
        }}

        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] label {{
            color: {c["text_muted"]};
        }}

        .aegis-topbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            height: 3.65rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1.25rem 0 1rem;
            background: {c["bg"]};
            border-bottom: 1px solid {c["border"]};
            box-shadow: 0 1px 0 rgba(0, 217, 255, 0.12);
        }}

        .aegis-topbar-left {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .aegis-logo {{
            width: 2.25rem;
            height: 2.25rem;
        }}

        .aegis-logo-simple {{
            width: 2.25rem;
            height: 2.5rem;
            flex-shrink: 0;
            background: linear-gradient(180deg, #081A2B 0%, #06111F 100%);
            border: 1.5px solid #00D9FF;
            border-radius: 6px 6px 10px 10px;
            clip-path: polygon(50% 0%, 100% 18%, 100% 72%, 50% 100%, 0% 72%, 0% 18%);
            box-shadow: 0 0 8px rgba(0, 217, 255, 0.25);
        }}

        .aegis-topbar-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: {c["text"]};
            line-height: 1.2;
        }}

        .aegis-topbar-sub {{
            font-size: 0.72rem;
            color: {c["text_muted"]};
        }}

        .aegis-topbar-right {{
            display: flex;
            align-items: center;
            gap: 0.85rem;
            font-size: 0.8rem;
            color: {c["text_muted"]};
        }}

        .aegis-topbar-chip {{
            background: {c["panel_alt"]};
            border: 1px solid {c["border"]};
            border-radius: 8px;
            padding: 0.35rem 0.65rem;
            color: {c["text"]};
        }}

        .aegis-topbar-icon {{
            width: 1.75rem;
            height: 1.75rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            border: 1px solid {c["border"]};
            background: {c["panel"]};
            color: {c["cyan"]};
            font-size: 0.85rem;
        }}

        .aegis-topbar-user {{
            color: {c["text"]};
            font-weight: 500;
        }}

        .aegis-nav-icon {{
            display: flex;
            align-items: center;
            color: {c["text_muted"]};
            padding-top: 0.45rem;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            text-align: left;
            justify-content: flex-start;
            background: transparent !important;
            border: 1px solid transparent !important;
            color: {c["text_muted"]} !important;
            border-radius: 8px !important;
            padding: 0.45rem 0.65rem !important;
            font-weight: 500 !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background: {c["panel_alt"]} !important;
            border-color: {c["border"]} !important;
            color: {c["text"]} !important;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
            background: {c["panel_alt"]} !important;
            border-left: 3px solid {c["cyan"]} !important;
            color: {c["text"]} !important;
        }}

        .aegis-sidebar-status {{
            margin-top: 1rem;
            padding: 0.65rem 0.75rem;
            background: {c["panel_alt"]};
            border: 1px solid {c["border"]};
            border-radius: 8px;
            font-size: 0.78rem;
            color: {c["text_muted"]};
        }}

        .aegis-sidebar-status strong {{
            color: {c["green"]};
            display: block;
            margin-bottom: 0.25rem;
        }}

        .aegis-banner-demo {{
            background: rgba(155, 92, 255, 0.12);
            border: 1px solid rgba(155, 92, 255, 0.35);
            color: {c["text"]};
            border-radius: 8px;
            padding: 0.55rem 0.85rem;
            font-size: 0.82rem;
            margin-bottom: 1rem;
        }}

        .aegis-page-header {{
            margin-bottom: 1.1rem;
        }}

        .aegis-page-title {{
            font-size: 1.65rem;
            font-weight: 700;
            color: {c["text"]};
            margin: 0 0 0.35rem 0;
        }}

        .aegis-page-desc {{
            color: {c["text_muted"]};
            font-size: 0.92rem;
            margin: 0;
        }}

        .aegis-metric-card {{
            background: {c["panel"]};
            border: 1px solid {c["border"]};
            border-radius: 8px;
            padding: 1rem 1.05rem;
            min-height: 118px;
        }}

        .aegis-metric-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .aegis-metric-label {{
            color: {c["text_muted"]};
            font-size: 0.82rem;
        }}

        .aegis-metric-icon {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .aegis-metric-value {{
            color: {c["text"]};
            font-size: 2rem;
            font-weight: 700;
            line-height: 1.15;
            margin-top: 0.35rem;
        }}

        .aegis-metric-delta {{
            font-size: 0.78rem;
            margin-top: 0.4rem;
        }}

        .aegis-panel {{
            background: {c["panel"]};
            border: 1px solid {c["border"]};
            border-radius: 8px;
            padding: 0.85rem 1rem;
        }}

        .aegis-panel-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: {c["text"]};
            margin: 0 0 0.75rem 0;
        }}

        .aegis-section-head {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 0.5rem 0 0.65rem 0;
        }}

        .aegis-section-head h3 {{
            margin: 0;
            font-size: 1rem;
            color: {c["text"]};
        }}

        .aegis-link {{
            color: {c["cyan"]};
            font-size: 0.85rem;
            text-decoration: none;
        }}

        .aegis-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
        }}

        .aegis-table th {{
            text-align: left;
            color: {c["text_muted"]};
            font-weight: 500;
            padding: 0.45rem 0.35rem;
            border-bottom: 1px solid {c["border"]};
        }}

        .aegis-table td {{
            padding: 0.55rem 0.35rem;
            border-bottom: 1px solid rgba(23, 59, 88, 0.55);
            color: {c["text"]};
        }}

        .aegis-progress-wrap {{
            height: 6px;
            background: {c["panel_alt"]};
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 0.2rem;
        }}

        .aegis-progress-bar {{
            height: 100%;
            border-radius: 999px;
        }}

        .aegis-progress-label {{
            font-size: 0.72rem;
            color: {c["text_muted"]};
        }}

        .aegis-status-ok {{
            background: rgba(0, 230, 160, 0.12);
            color: {c["green"]};
            padding: 0.15rem 0.45rem;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
        }}

        .aegis-result-list {{
            display: flex;
            flex-direction: column;
            gap: 0.65rem;
        }}

        .aegis-result-row {{
            display: flex;
            gap: 0.65rem;
            align-items: flex-start;
        }}

        .aegis-result-icon {{
            font-size: 0.9rem;
            margin-top: 0.15rem;
        }}

        .aegis-result-title {{
            font-size: 0.84rem;
            color: {c["text"]};
        }}

        .aegis-result-meta {{
            display: flex;
            gap: 0.65rem;
            font-size: 0.78rem;
            margin-top: 0.15rem;
        }}

        .aegis-result-time {{
            color: {c["text_muted"]};
        }}

        .aegis-ux-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.85rem;
            margin-top: 1.25rem;
        }}

        @media (max-width: 1100px) {{
            .aegis-ux-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .aegis-flow {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.75rem;
        }}

        .aegis-flow-step {{
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
            max-width: 5.5rem;
        }}

        .aegis-flow-step span {{
            color: {c["text_muted"]};
            font-size: 0.68rem;
        }}

        .aegis-flow-circle {{
            width: 1.65rem;
            height: 1.65rem;
            border-radius: 999px;
            border: 1px solid {c["cyan"]};
            color: {c["cyan"]};
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            margin-bottom: 0.15rem;
        }}

        .aegis-flow-arrow {{
            color: {c["border"]};
            font-size: 1rem;
        }}

        .aegis-checklist {{
            margin: 0;
            padding-left: 1.1rem;
            color: {c["text_muted"]};
            font-size: 0.8rem;
            line-height: 1.55;
        }}

        .aegis-checklist li::marker {{
            color: {c["green"]};
        }}

        .aegis-muted {{
            color: {c["text_muted"]};
            font-size: 0.8rem;
        }}

        .aegis-mini-form {{
            margin-top: 0.65rem;
        }}

        .aegis-mini-field {{
            background: {c["panel_alt"]};
            border: 1px solid {c["border"]};
            border-radius: 8px;
            padding: 0.45rem 0.55rem;
            font-size: 0.78rem;
            margin-bottom: 0.45rem;
        }}

        .aegis-mini-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            margin-bottom: 0.55rem;
        }}

        .aegis-chip {{
            font-size: 0.68rem;
            padding: 0.2rem 0.45rem;
            border-radius: 6px;
            border: 1px solid {c["border"]};
            color: {c["text_muted"]};
        }}

        .aegis-mini-cta {{
            display: inline-block;
            background: linear-gradient(90deg, {c["purple"]}, {c["cyan"]});
            color: {c["bg"]};
            font-weight: 600;
            font-size: 0.78rem;
            padding: 0.45rem 0.85rem;
            border-radius: 8px;
        }}

        .aegis-footer {{
            margin-top: 2rem;
            padding: 1rem 0 0.5rem;
            border-top: 1px solid {c["border"]};
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 0.75rem;
            font-size: 0.75rem;
            color: {c["text_muted"]};
        }}

        .aegis-footer-brand {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            color: {c["text"]};
            font-weight: 600;
        }}

        .aegis-footer-center {{
            color: {c["cyan"]};
        }}

        .aegis-footer-right {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 0.15rem;
            max-width: 22rem;
            text-align: right;
        }}

        .aegis-footer-muted {{
            font-size: 0.68rem;
        }}

        .stButton > button[kind="primary"]:not([data-testid="stSidebar"] button) {{
            background: linear-gradient(90deg, {c["purple"]}, #4cc9f0) !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: {c["bg"]} !important;
        }}

        div[data-testid="stExpander"] {{
            background: {c["panel"]};
            border: 1px solid {c["border"]};
            border-radius: 8px;
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid {c["border"]};
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
