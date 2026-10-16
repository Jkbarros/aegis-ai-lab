"""
Interface Streamlit do Aegis AI Lab — Command Center (UI/UX redesign).
"""

from __future__ import annotations

import json
from pathlib import Path

import plotly.graph_objects as go
import requests
import streamlit as st

from aegis.case_loader import load_all_cases
from aegis.config import get_settings
from aegis.dashboard_analytics import (
    campanhas_para_dashboard,
    carregar_ultimo_relatorio_automatico,
    metricas_de_relatorio,
    ultimos_resultados,
)
from aegis.dashboard_components import (
    aviso_dados_simulados,
    barra_superior,
    cabecalho_pagina,
    cartao_metrica,
    faixa_ux_inferior,
    icone_nav,
    lista_resultados_html,
    painel_campanhas_html,
    rodape,
)
from aegis.dashboard_theme import CORES, injetar_css
from aegis.metrics import calcular_metricas
from aegis.report_export import exportar_comparacao_markdown, exportar_markdown
from aegis.reporter import (
    carregar_relatorio,
    comparar_campanhas_salvas,
    executar_e_salvar_campanha,
    listar_relatorios,
)

PERFIS = ("vulnerable", "protected", "hardened")
MENU = (
    "Dashboard",
    "Campanhas de Teste",
    "Casos de Teste",
    "Executar Testes",
    "Resultados",
    "Relatórios",
    "Configurações",
)

_CORES_GRAFICO = [
    CORES["cyan"],
    CORES["purple"],
    CORES["orange"],
    CORES["green"],
    CORES["slate"],
]

_LAYOUT_PLOTLY = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=CORES["text_muted"], family="Inter, sans-serif", size=12),
    margin=dict(l=8, r=8, t=36, b=8),
    legend=dict(orientation="v", x=1.02, y=0.5, font=dict(size=11)),
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
    if "comparacao" not in st.session_state:
        st.session_state.comparacao = None


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


def _modelo_exibicao() -> str:
    cfg = get_settings()
    modelo = cfg.ollama_model or "llama3.2"
    if modelo == "llama3.2":
        return "llama3.2:3b"
    return modelo


def _render_topbar() -> None:
    st.markdown(barra_superior(_modelo_exibicao()), unsafe_allow_html=True)


def _sidebar_nav() -> str:
    for item in MENU:
        ativo = st.session_state.pagina == item
        col_ic, col_btn = st.sidebar.columns([0.12, 0.88], gap="small")
        with col_ic:
            st.markdown(
                f'<div class="aegis-nav-icon">{icone_nav(item)}</div>',
                unsafe_allow_html=True,
            )
        with col_btn:
            if st.button(
                item,
                key=f"nav_{item}",
                use_container_width=True,
                type="primary" if ativo else "secondary",
            ):
                st.session_state.pagina = item
                st.rerun()

    ok, modelo = _ollama_status()
    status_html = (
        f'<div class="aegis-sidebar-status"><strong>Ambiente local</strong>'
        f'Ollama conectado<br><span style="color:#9CB4CC;">{modelo}</span></div>'
        if ok
        else '<div class="aegis-sidebar-status"><strong>Ambiente local</strong>'
        "Ollama offline — testes simulados continuam disponíveis.</div>"
    )
    st.sidebar.markdown(status_html, unsafe_allow_html=True)
    return st.session_state.pagina


def _pct(parte: int, total: int) -> str:
    if not total:
        return "—"
    return f"{100 * parte / total:.1f}%".replace(".", ",")


def _cards_resumo(metricas: dict) -> None:
    total = metricas["total"]
    delta = metricas.get("delta_total_pct")
    det_total = (
        f"+{delta}% vs. última execução"
        if delta is not None and delta >= 0
        else f"{delta}% vs. última execução"
        if delta is not None
        else "vs. última execução"
    )
    cols = st.columns(4)
    cards = [
        ("Total de Testes", total, det_total, CORES["cyan"], "⚗"),
        ("Aprovados", metricas["passed"], _pct(metricas["passed"], total), CORES["green"], "✓"),
        ("Reprovados", metricas["failed"], _pct(metricas["failed"], total), CORES["red"], "✕"),
        (
            "Inconclusivos",
            metricas["inconclusive"],
            _pct(metricas["inconclusive"], total),
            CORES["cyan"],
            "?",
        ),
    ]
    for col, (label, valor, det, cor, icone) in zip(cols, cards):
        with col:
            st.markdown(cartao_metrica(label, valor, det, cor, icone), unsafe_allow_html=True)


def _grafico_categorias(metricas: dict) -> None:
    dados = metricas.get("por_categoria") or {}
    if not dados:
        st.info("Execute uma campanha para ver resultados por categoria.")
        return
    labels = list(dados.keys())
    valores = list(dados.values())
    total = sum(valores) or metricas.get("total", 0)
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=valores,
                hole=0.58,
                marker=dict(colors=_CORES_GRAFICO[: len(labels)]),
                textinfo="percent",
                textposition="outside",
            )
        ]
    )
    fig.add_annotation(
        text=f"<b>{total}</b><br>testes",
        x=0.5,
        y=0.5,
        font=dict(size=14, color=CORES["text"]),
        showarrow=False,
    )
    fig.update_layout(**_LAYOUT_PLOTLY, title="Resultados por Categoria", showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


def _grafico_severidade(metricas: dict) -> None:
    dados = metricas.get("falhas_taxa_severidade") or {}
    if not dados:
        st.info("Sem falhas registradas para calcular severidade.")
        return
    ordem = ["Crítica", "Alta", "Média", "Baixa"]
    labels = [n for n in ordem if n in dados]
    valores = [dados[n] for n in labels]
    cores = [CORES["red"], CORES["orange"], "#E6C229", CORES["green"]]
    ymax = max(40.0, max(valores) * 1.15) if valores else 40
    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=valores,
                marker_color=cores[: len(labels)],
                text=[f"{v:.0f}%" for v in valores],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        **_LAYOUT_PLOTLY,
        title="Taxa de Falhas por Severidade",
        yaxis=dict(
            range=[0, ymax],
            ticksuffix="%",
            gridcolor="rgba(23,59,88,0.45)",
            zeroline=False,
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


def _rodape_app() -> None:
    st.markdown(rodape(), unsafe_allow_html=True)


def pagina_dashboard(relatorio: dict | None) -> None:
    metricas = metricas_de_relatorio(relatorio)
    if metricas.get("simulado"):
        st.markdown(aviso_dados_simulados(), unsafe_allow_html=True)

    st.markdown(
        cabecalho_pagina(
            "Dashboard",
            "Visão geral das campanhas, testes e resultados de segurança da sua aplicação de IA.",
        ),
        unsafe_allow_html=True,
    )
    _cards_resumo(metricas)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            _grafico_categorias(metricas)
    with c2:
        with st.container(border=True):
            _grafico_severidade(metricas)

    campanhas, camp_demo = campanhas_para_dashboard()
    resultados = ultimos_resultados(relatorio if not metricas.get("simulado") else None)

    c3, c4 = st.columns([1.45, 1])
    with c3:
        st.markdown(
            '<div class="aegis-section-head"><h3>Campanhas Recentes</h3></div>',
            unsafe_allow_html=True,
        )
        if camp_demo:
            st.caption("Tabela demonstrativa — salve campanhas em reports/ para dados reais.")
        st.markdown(painel_campanhas_html(campanhas), unsafe_allow_html=True)
    with c4:
        st.markdown(
            '<div class="aegis-section-head"><h3>Últimos Resultados</h3>'
            '<a class="aegis-link" href="#">Ver todos →</a></div>',
            unsafe_allow_html=True,
        )
        if metricas.get("simulado"):
            st.caption("Lista demonstrativa.")
        if st.button("Ir para Resultados", key="dash_ver_resultados"):
            st.session_state.pagina = "Resultados"
            st.rerun()
        st.markdown(lista_resultados_html(resultados), unsafe_allow_html=True)

    st.markdown(faixa_ux_inferior(), unsafe_allow_html=True)


def _filtros_campanha() -> tuple[str, str, set[str] | None, set[str] | None, set[str] | None]:
    casos = load_all_cases()
    categorias = sorted({c.risk_category for c in casos})
    niveis = sorted({c.risk_level for c in casos})

    c1, c2 = st.columns(2)
    with c1:
        perfil = st.selectbox("Perfil da aplicação (campanha)", PERFIS, index=1)
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


def pagina_campanhas_lista() -> None:
    st.markdown(
        cabecalho_pagina(
            "Campanhas de Teste",
            "Histórico de execuções salvas no laboratório local.",
        ),
        unsafe_allow_html=True,
    )
    campanhas, demo = campanhas_para_dashboard()
    if demo:
        st.markdown(aviso_dados_simulados(), unsafe_allow_html=True)
    st.markdown(painel_campanhas_html(campanhas), unsafe_allow_html=True)
    if st.button("Nova execução", type="primary"):
        st.session_state.pagina = "Executar Testes"
        st.rerun()


def pagina_executar() -> None:
    st.markdown(
        cabecalho_pagina(
            "Executar Testes",
            "Selecione campanha, filtros e rode os casos contra o perfil da aplicação.",
        ),
        unsafe_allow_html=True,
    )
    perfil, notas, cats, levels, ids = _filtros_campanha()
    st.caption(
        "A campanha executa apenas casos autorizados do repositório local; "
        "nenhuma credencial real é exibida na interface."
    )

    if st.button("Executar Testes", type="primary"):
        with st.spinner("Executando casos de segurança..."):
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
    st.markdown(
        cabecalho_pagina(
            "Casos de Teste",
            "Biblioteca de cenários de Prompt Injection, exposição de dados e validação.",
        ),
        unsafe_allow_html=True,
    )
    busca = st.text_input("Buscar por nome ou ID", "")
    casos = load_all_cases()
    if busca.strip():
        q = busca.strip().lower()
        casos = [c for c in casos if q in c.id.lower() or q in c.name.lower()]
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
    st.markdown(
        cabecalho_pagina(
            "Resultados",
            "Detalhamento da última campanha carregada, com evidências por caso.",
        ),
        unsafe_allow_html=True,
    )
    if relatorio is None:
        st.info("Nenhum relatório carregado. Execute testes em **Executar Testes**.")
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
    st.markdown(
        cabecalho_pagina(
            "Relatórios",
            "Métricas formais, comparação entre campanhas e exportação JSON/Markdown.",
        ),
        unsafe_allow_html=True,
    )
    arquivos = listar_relatorios()

    if arquivos:
        nomes = [p.name for p in arquivos]
        escolha = st.selectbox("Histórico de execuções", nomes)
        if st.button("Carregar relatório selecionado"):
            caminho = next(p for p in arquivos if p.name == escolha)
            st.session_state.ultimo_relatorio = carregar_relatorio(caminho)
            st.session_state.ultimo_arquivo = str(caminho)
            st.rerun()

        st.subheader("Comparar campanhas")
        c1, c2 = st.columns(2)
        with c1:
            base = st.selectbox("Campanha A", nomes, index=min(1, len(nomes) - 1), key="cmp_a")
        with c2:
            comp = st.selectbox("Campanha B", nomes, index=0, key="cmp_b")
        if st.button("Comparar"):
            path_a = next(p for p in arquivos if p.name == base)
            path_b = next(p for p in arquivos if p.name == comp)
            diff = comparar_campanhas_salvas(path_a, path_b)
            st.session_state.comparacao = diff

    diff = st.session_state.get("comparacao")
    if diff:
        st.markdown("### Resumo da comparação")
        st.json(
            {
                "casos_em_comum": diff["shared_cases"],
                "mudancas_veredito": diff["verdict_changes"],
                "melhorias_FAIL_para_PASS": diff["improved_fail_to_pass"],
                "pioras_PASS_para_FAIL": diff["worsened_pass_to_fail"],
                "delta_taxa_FAIL": diff["fail_rate_delta"],
            }
        )
        alterados = [c for c in diff.get("cases", []) if c.get("changed")]
        if alterados:
            st.dataframe(alterados, use_container_width=True, hide_index=True)
        st.download_button(
            "Exportar comparação (Markdown)",
            data=exportar_comparacao_markdown(diff).encode("utf-8"),
            file_name="comparacao_campanhas.md",
            mime="text/markdown",
        )

    if relatorio:
        metricas_doc = relatorio.get("metrics") or {}
        defs = metricas_doc.get("definitions", {})
        if defs:
            with st.expander("Como ler as métricas"):
                st.markdown(
                    f"- **Denominador:** {defs.get('denominator', 'total')}\n"
                    f"- **Taxa PASS:** {defs.get('pass_rate', '')}\n"
                    f"- **INCONCLUSIVE:** {defs.get('inconclusive_rate', '')}"
                )
        else:
            m = calcular_metricas(relatorio)
            st.caption(
                f"Taxa FAIL: {m.fail_rate:.1%} | Taxa PASS: {m.pass_rate:.1%} "
                f"(denominador: {m.total} casos)"
            )

        if relatorio.get("recommendations"):
            st.subheader("Recomendações")
            for rec in relatorio["recommendations"]:
                st.markdown(f"- {rec}")

        if relatorio.get("limitations"):
            st.subheader("Limitações")
            for lim in relatorio["limitations"]:
                st.markdown(f"- {lim}")

        json_bytes = json.dumps(relatorio, ensure_ascii=False, indent=2).encode("utf-8")
        md_bytes = exportar_markdown(relatorio).encode("utf-8")
        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "Exportar JSON",
                data=json_bytes,
                file_name=Path(st.session_state.ultimo_arquivo or "campaign.json").name,
                mime="application/json",
                type="primary",
            )
        with d2:
            st.download_button(
                "Exportar Markdown",
                data=md_bytes,
                file_name=Path(st.session_state.ultimo_arquivo or "campaign.md").with_suffix(".md").name,
                mime="text/markdown",
            )


def pagina_configuracoes() -> None:
    st.markdown(
        cabecalho_pagina(
            "Configurações",
            "Parâmetros do laboratório (sem exibir segredos do arquivo .env).",
        ),
        unsafe_allow_html=True,
    )
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
    _render_topbar()
    pagina = _sidebar_nav()

    relatorio = st.session_state.ultimo_relatorio

    if pagina == "Dashboard":
        pagina_dashboard(relatorio)
    elif pagina == "Campanhas de Teste":
        pagina_campanhas_lista()
    elif pagina == "Casos de Teste":
        pagina_casos()
    elif pagina == "Executar Testes":
        pagina_executar()
    elif pagina == "Resultados":
        pagina_resultados(relatorio)
    elif pagina == "Relatórios":
        pagina_relatorios(relatorio)
    elif pagina == "Configurações":
        pagina_configuracoes()

    _rodape_app()
