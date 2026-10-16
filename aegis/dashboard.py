"""
Interface Streamlit do Aegis AI Lab (Etapa 8).
"""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from aegis.case_loader import load_all_cases
from aegis.reporter import (
    carregar_relatorio,
    executar_e_salvar_campanha,
    listar_relatorios,
    montar_relatorio,
    salvar_relatorio,
)
from aegis.test_runner import TestRunner


PERFIS = ("vulnerable", "protected", "hardened")


def _inicializar_estado() -> None:
    if "ultimo_relatorio" not in st.session_state:
        st.session_state.ultimo_relatorio = None
    if "ultimo_arquivo" not in st.session_state:
        st.session_state.ultimo_arquivo = None


def _opcoes_filtro() -> tuple[set[str] | None, set[str] | None, set[str] | None]:
    casos = load_all_cases()
    categorias = sorted({c.risk_category for c in casos})
    niveis = sorted({c.risk_level for c in casos})

    sel_cat = st.sidebar.multiselect("Categorias de risco", categorias, default=categorias)
    sel_nivel = st.sidebar.multiselect("Nível de risco", niveis, default=niveis)
    sel_ids = st.sidebar.multiselect(
        "Casos específicos (opcional)",
        options=[f"{c.id} — {c.name}" for c in casos],
        default=[],
    )

    cats = set(sel_cat) if sel_cat else None
    levels = set(sel_nivel) if sel_nivel else None
    ids = {item.split(" — ", 1)[0] for item in sel_ids} if sel_ids else None
    return cats, levels, ids


def _mostrar_resumo(relatorio: dict) -> None:
    resumo = relatorio.get("summary", {})
    cols = st.columns(5)
    cols[0].metric("Total", resumo.get("total", 0))
    cols[1].metric("PASS", resumo.get("passed", 0))
    cols[2].metric("FAIL", resumo.get("failed", 0))
    cols[3].metric("ERROR", resumo.get("errors", 0))
    cols[4].metric("INCONCLUSIVE", resumo.get("inconclusive", 0))

    if resumo.get("expectation_mismatches", 0) > 0:
        st.warning(
            f"Divergências vs expectations do JSON: {resumo['expectation_mismatches']}"
        )


def _mostrar_tabela(relatorio: dict) -> None:
    linhas = []
    for item in relatorio.get("results", []):
        linhas.append(
            {
                "ID": item.get("case_id"),
                "Nome": item.get("case_name"),
                "Categoria": item.get("risk_category"),
                "Nível": item.get("risk_level"),
                "Veredito": item.get("verdict"),
                "Esperado": item.get("expected_verdict") or "-",
                "OK expect.": item.get("expectation_met"),
            }
        )
    if linhas:
        st.dataframe(linhas, use_container_width=True, hide_index=True)

    for item in relatorio.get("results", []):
        titulo = f"{item.get('case_id')} — {item.get('verdict')}"
        with st.expander(titulo):
            st.markdown(f"**Entrada:** {item.get('user_input')}")
            st.markdown(f"**Resposta:** {item.get('response_text')}")
            st.markdown(f"**Resumo:** {item.get('summary')}")
            if item.get("evidence"):
                st.json(item["evidence"])


def render() -> None:
    """Ponto de entrada da UI Streamlit."""
    st.set_page_config(
        page_title="Aegis AI Lab",
        page_icon="🛡️",
        layout="wide",
    )
    _inicializar_estado()

    st.title("Aegis AI Lab")
    st.caption(
        "Laboratório local de testes de segurança em aplicações com LLM. "
        "Use apenas em ambientes autorizados."
    )

    st.sidebar.header("Campanha")
    perfil = st.sidebar.selectbox("Perfil da aplicação", PERFIS, index=1)
    notas = st.sidebar.text_input("Notas da execução (opcional)", "")
    cats, levels, ids = _opcoes_filtro()

    if st.sidebar.button("Executar campanha", type="primary"):
        with st.spinner("Executando casos..."):
            relatorio, caminho = executar_e_salvar_campanha(
                perfil,
                categories=cats,
                risk_levels=levels,
                case_ids=ids,
                notas=notas,
            )
        st.session_state.ultimo_relatorio = relatorio
        st.session_state.ultimo_arquivo = str(caminho)
        st.success(f"Campanha salva em: {caminho.name}")

    st.sidebar.divider()
    st.sidebar.header("Histórico")
    arquivos = listar_relatorios()
    if arquivos:
        labels = [p.name for p in arquivos]
        escolha = st.sidebar.selectbox("Relatório salvo", labels)
        if st.sidebar.button("Carregar relatório"):
            caminho = next(p for p in arquivos if p.name == escolha)
            st.session_state.ultimo_relatorio = carregar_relatorio(caminho)
            st.session_state.ultimo_arquivo = str(caminho)
    else:
        st.sidebar.info("Nenhum relatório em reports/ ainda.")

    relatorio = st.session_state.ultimo_relatorio
    if relatorio is None:
        st.info("Execute uma campanha na barra lateral ou carregue um relatório do histórico.")
        return

    st.subheader(f"Perfil: {relatorio.get('campaign', {}).get('profile', '?')}")
    meta = relatorio.get("lab", {})
    st.caption(
        f"Gerado em {relatorio.get('generated_at', '?')} | "
        f"Provedor: {meta.get('llm_provider', '?')}"
    )

    _mostrar_resumo(relatorio)
    st.subheader("Resultados")
    _mostrar_tabela(relatorio)

    json_bytes = json.dumps(relatorio, ensure_ascii=False, indent=2).encode("utf-8")
    st.download_button(
        "Exportar JSON",
        data=json_bytes,
        file_name=Path(st.session_state.ultimo_arquivo or "campaign.json").name,
        mime="application/json",
    )
