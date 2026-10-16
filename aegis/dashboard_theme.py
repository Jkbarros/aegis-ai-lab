"""Tema visual do dashboard (inspirado no mockup cyber/dark)."""

from __future__ import annotations

import streamlit as st

CORES = {
    "bg": "#0b1120",
    "card": "#111827",
    "border": "#1e293b",
    "teal": "#14b8a6",
    "purple": "#8b5cf6",
    "red": "#ef4444",
    "amber": "#f59e0b",
    "blue": "#3b82f6",
    "green": "#22c55e",
}


def injetar_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {CORES["bg"]};
        }}
        [data-testid="stSidebar"] {{
            background-color: #0f172a;
            border-right: 1px solid {CORES["border"]};
        }}
        .aegis-brand {{
            font-size: 1.35rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 0.1rem;
        }}
        .aegis-sub {{
            font-size: 0.78rem;
            color: #94a3b8;
            margin-bottom: 1.2rem;
        }}
        .aegis-metric-card {{
            background: {CORES["card"]};
            border: 1px solid {CORES["border"]};
            border-radius: 12px;
            padding: 1rem 1.1rem;
            min-height: 110px;
        }}
        .aegis-metric-label {{
            color: #94a3b8;
            font-size: 0.85rem;
            margin-bottom: 0.35rem;
        }}
        .aegis-metric-value {{
            color: #f8fafc;
            font-size: 2rem;
            font-weight: 700;
            line-height: 1.1;
        }}
        .aegis-metric-delta {{
            font-size: 0.8rem;
            margin-top: 0.35rem;
        }}
        .aegis-panel {{
            background: {CORES["card"]};
            border: 1px solid {CORES["border"]};
            border-radius: 12px;
            padding: 1rem;
        }}
        .aegis-header-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}
        .aegis-pill {{
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        div[data-testid="stMetric"] {{
            background: {CORES["card"]};
            border: 1px solid {CORES["border"]};
            border-radius: 12px;
            padding: 0.75rem;
        }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(90deg, #7c3aed, #6366f1);
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def cartao_metrica(label: str, valor: str | int, detalhe: str, cor: str) -> str:
    return f"""
    <div class="aegis-metric-card" style="border-top: 3px solid {cor};">
        <div class="aegis-metric-label">{label}</div>
        <div class="aegis-metric-value">{valor}</div>
        <div class="aegis-metric-delta" style="color:{cor};">{detalhe}</div>
    </div>
    """
