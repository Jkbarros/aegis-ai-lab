"""
Interface Streamlit do Aegis AI Lab — UI dark/cyber (Etapa 8+).
"""

from __future__ import annotations

import json
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

from aegis.case_loader import load_all_cases
from aegis.config import get_settings
from aegis.dashboard_analytics import (
    carregar_ultimo_relatorio_automatico,
    listar_campanhas_resumo,
    metricas_de_relatorio,
    ultimos_resultados,
)
from aegis.dashboard_theme import CORES, cartao_metrica, injetar_css
from aegis.reporter import carregar_relatorio, executar_e_salvar_campanha, listar_relatorios

PERFIS = ("vulnerable", "protected", "hardened")
MENU = (
    "Dashboard",
    "Campanhas de Teste",
    "Casos de Teste",
    "Resultados",
    "Relatórios",
    "Configurações",
)

_LAYOUT_PLOTLY = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cbd5e1"),
    margin=dict(l=10, r=10, t=40, b=10),
)


def _inicializar_estado() -> None:
    if "ultimo_relatorio" not in st.session_state:
        rel, path = carregar_ultimo_relatorio_automatico()
        st.session_state.ultimo_relatorio = rel
        st.session_state.ultimo_arquivo = path
    if "ultimo_arquivo" not in st.session_state:
        st.session_state.ultimo_arquivo = None
    if "pagina" not in st.session_state:
        st.session_state.pagina = MENU[0]


def _ollama_status() -> tuple[bool, str]:
    cfg = get_settings()
    url = cfg.ollama_base_url.rstrip("/")
    try:
        res = requests.get(f"{url}/api/tags", timeout=2)
        if res.status_code == 200:
            return True, cfg.ollama_model
    except requests.RequestException:
        pass
    return False, cfg.ollama_model


def _sidebar_nav() -> str:
    st.sidebar.markdown('<div class="aegis-brand">Aegis AI Lab</div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="aegis-sub">Laboratório de Segurança para Aplicações de IA</div>',
        unsafe_allow_html=True,
    )

    for item in MENU:
        ativo = st.session_state.pagina == item
        if st.sidebar.button(
            item,
            key=f"nav_{item}",
            use_container_width=True,
            type="primary" if ativo else "secondary",
        ):
            st.session_state.pagina = item

    st.sidebar.markdown("---")
    ok, modelo = _ollama_status()
    if ok:
        st.sidebar.success(f"Ollama conectado ({modelo})")
    else:
        st.sidebar.warning("Ollama offline ou indisponível")
    st.sidebar.caption("Ambiente local autorizado")
    return st.session_state.pagina


def _header_topo() -> None:
    cfg = get_settings()
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.markdown("## Dashboard de Segurança")
        st.caption("Visão geral dos testes de segurança em aplicações de IA")
    with col2:
        st.selectbox(
            "Modelo",
            [cfg.ollama_model, cfg.openai_model],
            label_visibility="collapsed",
        )
    with col3:
        st.markdown(
            '<div style="text-align:right;padding-top:0.5rem;">'
            '<span class="aegis-pill" style="background:#1e293b;color:#e2e8f0;">'
            "Usuário Local</span></div>",
            unsafe_allow_html=True,
        )


def _cards_resumo(metricas: dict) -> None:
    total = metricas["total"]
    taxa_ok = f"{int(100 * metricas['passed'] / total)}%" if total else "—"
    cols = st.columns(4)
    cards = [
        ("Total de Testes", total, f"{taxa_ok} aprovados", CORES["teal"]),
        ("Aprovados", metricas["passed"], "PASS", CORES["green"]),
        ("Reprovados", metricas["failed"], "FAIL", CORES["red"]),
        ("Inconclusivos", metricas["inconclusive"], "Revisão humana", CORES["blue"]),
    ]
    for col, (label, valor, det, cor) in zip(cols, cards):
        with col:
            st.markdown(cartao_metrica(label, valor, det, cor), unsafe_allow_html=True)


def _grafico_categorias(metricas: dict) -> None:
    dados = metricas.get("por_categoria") or {}
    if not dados:
        st.info("Execute uma campanha para ver resultados por categoria.")
        return
    fig = px.pie(
        names=list(dados.keys()),
        values=list(dados.values()),
        hole=0.55,
        color_discrete_sequence=[CORES["teal"], CORES["purple"], CORES["blue"], CORES["amber"]],
    )
    fig.update_layout(**_LAYOUT_PLOTLY, title="Resultados por Categoria")
    st.plotly_chart(fig, use_container_width=True)


def _grafico_severidade(metricas: dict) -> None:
    dados = metricas.get("falhas_por_nivel") or {}
    niveis = ["critical", "high", "medium", "low"]
    valores = [dados.get(n, 0) for n in niveis]
    cores = [CORES["red"], CORES["amber"], "#eab308", CORES["green"]]
    fig = go.Figure(
        data=[
            go.Bar(
                x=["Crítico", "Alto", "Médio", "Baixo"],
                y=valores,
                marker_color=cores,
            )
        ]
    )
    fig.update_layout(**_LAYOUT_PLOTLY, title="Falhas por Severidade (FAIL)")
    st.plotly_chart(fig, use_container_width=True)


def _tabela_campanhas() -> None:
    linhas = listar_campanhas_resumo()
    if not linhas:
        st.caption("Nenhuma campanha salva em reports/ ainda.")
        return
    st.dataframe(
        [
            {
                "Campanha": r["nome"],
                "Data": r["data"],
                "Testes": r["testes"],
                "% PASS": f"{r['pass_pct']}%",
                "Perfil": r["perfil"],
                "Status": r["status"],
            }
            for r in linhas
        ],
        use_container_width=True,
        hide_index=True,
    )


def _lista_ultimos(relatorio: dict | None) -> None:
    for item in ultimos_resultados(relatorio):
        cor = {
            "PASS": CORES["green"],
            "FAIL": CORES["red"],
            "ERROR": CORES["amber"],
            "INCONCLUSIVE": CORES["blue"],
        }.get(item["verdict"], "#94a3b8")
        st.markdown(
            f"- **{item['id']}** — {item['nome']} "
            f"<span style='color:{cor};font-weight:600;'>{item['verdict']}</span>",
            unsafe_allow_html=True,
        )


def pagina_dashboard(relatorio: dict | None) -> None:
    _header_topo()
    metricas = metricas_de_relatorio(relatorio)
    _cards_resumo(metricas)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            _grafico_categorias(metricas)
    with c2:
        with st.container(border=True):
            _grafico_severidade(metricas)

    c3, c4 = st.columns([1.4, 1])
    with c3:
        st.subheader("Campanhas Recentes")
        _tabela_campanhas()
    with c4:
        st.subheader("Últimos Resultados")
        _lista_ultimos(relatorio)


def _filtros_campanha() -> tuple[str, str, set[str] | None, set[str] | None, set[str] | None]:
    casos = load_all_cases()
    categorias = sorted({c.risk_category for c in casos})
    niveis = sorted({c.risk_level for c in casos})

    c1, c2 = st.columns(2)
    with c1:
        perfil = st.selectbox("Perfil da aplicação", PERFIS, index=1)
    with c2:
        notas = st.text_input("Notas da execução", "")

    sel_cat = st.multiselect("Tipos de teste (categorias)", categorias, default=categorias)
    sel_nivel = st.multiselect("Níveis de risco", niveis, default=niveis)
    sel_ids = st.multiselect(
        "Casos específicos (opcional)",
        [f"{c.id} — {c.name}" for c in casos],
        default=[],
    )

    cats = set(sel_cat) if sel_cat else None
    levels = set(sel_nivel) if sel_nivel else None
    ids = {x.split(" — ", 1)[0] for x in sel_ids} if sel_ids else None
    return perfil, notas, cats, levels, ids


def pagina_campanhas() -> None:
    st.markdown("## Campanhas de Teste")
    st.caption("Selecione perfil e filtros, depois execute a campanha.")

    perfil, notas, cats, levels, ids = _filtros_campanha()

    if st.button("Executar Testes", type="primary"):
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
        st.success(f"Campanha concluída e salva: {caminho.name}")
        st.session_state.pagina = "Resultados"
        st.rerun()


def pagina_casos() -> None:
    st.markdown("## Biblioteca de Casos de Teste")
    casos = load_all_cases()
    st.dataframe(
        [
            {
                "ID": c.id,
                "Nome": c.name,
                "Categoria": c.risk_category,
                "Nível": c.risk_level,
                "Objetivo": c.objective[:80] + ("..." if len(c.objective) > 80 else ""),
            }
            for c in casos
        ],
        use_container_width=True,
        hide_index=True,
    )


def pagina_resultados(relatorio: dict | None) -> None:
    st.markdown("## Resultados da Campanha")
    if relatorio is None:
        st.info("Nenhum relatório carregado. Execute uma campanha em **Campanhas de Teste**.")
        return

    meta = relatorio.get("lab", {})
    st.caption(
        f"Perfil: {relatorio.get('campaign', {}).get('profile')} | "
        f"Gerado: {relatorio.get('generated_at')} | Provedor: {meta.get('llm_provider')}"
    )
    _cards_resumo(metricas_de_relatorio(relatorio))

    for item in relatorio.get("results", []):
        verdict = item.get("verdict")
        with st.expander(f"{item.get('case_id')} — {item.get('case_name')} [{verdict}]"):
            st.markdown(f"**Entrada:** {item.get('user_input')}")
            st.markdown(f"**Resposta:** {item.get('response_text')}")
            st.markdown(f"**Resumo:** {item.get('summary')}")
            if item.get("evidence"):
                st.json(item["evidence"])


def pagina_relatorios(relatorio: dict | None) -> None:
    st.markdown("## Relatórios")
    arquivos = listar_relatorios()
    if arquivos:
        nomes = [p.name for p in arquivos]
        escolha = st.selectbox("Histórico de execuções", nomes)
        if st.button("Carregar relatório selecionado"):
            caminho = next(p for p in arquivos if p.name == escolha)
            st.session_state.ultimo_relatorio = carregar_relatorio(caminho)
            st.session_state.ultimo_arquivo = str(caminho)
            st.rerun()

    if relatorio:
        json_bytes = json.dumps(relatorio, ensure_ascii=False, indent=2).encode("utf-8")
        st.download_button(
            "Exportar JSON",
            data=json_bytes,
            file_name=Path(st.session_state.ultimo_arquivo or "campaign.json").name,
            mime="application/json",
            type="primary",
        )


def pagina_configuracoes() -> None:
    st.markdown("## Configurações")
    cfg = get_settings()
    st.json(
        {
            "llm_provider": cfg.llm_provider,
            "ollama_base_url": cfg.ollama_base_url,
            "ollama_model": cfg.ollama_model,
            "openai_model": cfg.openai_model,
            "openai_api_key_configurada": bool(cfg.openai_api_key),
            "lab_fake_secret_definido": bool(cfg.lab_fake_secret),
        }
    )
    st.warning("Chaves reais ficam apenas no arquivo .env local (não versionado).")


def render() -> None:
    st.set_page_config(
        page_title="Aegis AI Lab",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    injetar_css()
    _inicializar_estado()
    pagina = _sidebar_nav()

    relatorio = st.session_state.ultimo_relatorio

    if pagina == "Dashboard":
        pagina_dashboard(relatorio)
    elif pagina == "Campanhas de Teste":
        pagina_campanhas()
    elif pagina == "Casos de Teste":
        pagina_casos()
    elif pagina == "Resultados":
        pagina_resultados(relatorio)
    elif pagina == "Relatórios":
        pagina_relatorios(relatorio)
    elif pagina == "Configurações":
        pagina_configuracoes()
