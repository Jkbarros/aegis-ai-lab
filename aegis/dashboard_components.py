"""Componentes HTML reutilizáveis do dashboard Streamlit."""

from __future__ import annotations

from aegis.dashboard_theme import CORES

def icone_nav(nome: str) -> str:
    """Ícones lineares minimalistas (SVG inline)."""
    icons = {
        "Dashboard": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
        "Campanhas de Teste": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 6h16M4 12h10M4 18h14"/></svg>',
        "Casos de Teste": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/></svg>',
        "Executar Testes": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="8,5 19,12 8,19"/></svg>',
        "Resultados": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19h16M6 16l4-5 4 3 5-7"/></svg>',
        "Relatórios": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 3h7l5 5v13a1 1 0 01-1 1H7a1 1 0 01-1-1V4a1 1 0 011-1z"/><path d="M14 3v5h5"/></svg>',
        "Configurações": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    }
    return icons.get(nome, "")


def barra_superior(modelo_llm: str, usuario: str = "Usuário Local") -> str:
    return f"""
    <div class="aegis-topbar">
      <div class="aegis-topbar-left">
        <div class="aegis-logo-simple" aria-hidden="true"></div>
        <div class="aegis-topbar-titles">
          <div class="aegis-topbar-title">Aegis AI Lab</div>
          <div class="aegis-topbar-sub">Laboratório de Segurança para Aplicações de IA</div>
        </div>
      </div>
      <div class="aegis-topbar-right">
        <span class="aegis-topbar-chip">Modelo: {modelo_llm}</span>
        <span class="aegis-topbar-icon" title="Tema">◐</span>
        <span class="aegis-topbar-icon" title="Conta">◉</span>
        <span class="aegis-topbar-user">{usuario}</span>
      </div>
    </div>
    """


def aviso_dados_simulados() -> str:
    return """
    <div class="aegis-banner-demo">
      Dados demonstrativos (simulados) — execute uma campanha para substituir por resultados reais do laboratório.
    </div>
    """


def cabecalho_pagina(titulo: str, descricao: str) -> str:
    return f"""
    <div class="aegis-page-header">
      <h1 class="aegis-page-title">{titulo}</h1>
      <p class="aegis-page-desc">{descricao}</p>
    </div>
    """


def cartao_metrica(
    label: str,
    valor: str | int,
    detalhe: str,
    cor: str,
    icone: str = "",
) -> str:
    return f"""
    <div class="aegis-metric-card">
      <div class="aegis-metric-top">
        <span class="aegis-metric-label">{label}</span>
        <span class="aegis-metric-icon" style="color:{cor};">{icone}</span>
      </div>
      <div class="aegis-metric-value">{valor}</div>
      <div class="aegis-metric-delta" style="color:{CORES['text_muted']};">{detalhe}</div>
    </div>
    """


def painel_campanhas_html(linhas: list[dict]) -> str:
    rows = []
    for r in linhas:
        pct = r.get("pass_pct", 0)
        cor_bar = CORES["green"] if pct >= 70 else CORES["cyan"] if pct >= 40 else CORES["red"]
        rows.append(
            f"""
            <tr>
              <td>{r.get("nome", "—")}</td>
              <td>{r.get("data", "—")}</td>
              <td>{r.get("testes", "—")}</td>
              <td>
                <div class="aegis-progress-wrap">
                  <div class="aegis-progress-bar" style="width:{pct}%;background:{cor_bar};"></div>
                </div>
                <span class="aegis-progress-label">{pct}% PASS</span>
              </td>
              <td><span class="aegis-status-ok">{r.get("status", "Concluída")}</span></td>
            </tr>
            """
        )
    body = "\n".join(rows) if rows else "<tr><td colspan='5'>Nenhuma campanha salva.</td></tr>"
    return f"""
    <div class="aegis-panel">
      <table class="aegis-table">
        <thead>
          <tr><th>Nome</th><th>Data</th><th>Testes</th><th>Resultado</th><th>Status</th></tr>
        </thead>
        <tbody>{body}</tbody>
      </table>
    </div>
    """


def lista_resultados_html(itens: list[dict]) -> str:
    def _cor(verdict: str) -> str:
        mapa = {
            "PASS": CORES["green"],
            "FAIL": CORES["red"],
            "INCONCLUSIVE": CORES["cyan"],
            "ERROR": CORES["orange"],
            "Aprovado": CORES["green"],
            "Falha": CORES["red"],
            "Inconclusivo": CORES["cyan"],
        }
        return mapa.get(verdict, CORES["text_muted"])

    def _label(verdict: str) -> str:
        mapa = {
            "PASS": "Aprovado",
            "FAIL": "Falha",
            "INCONCLUSIVE": "Inconclusivo",
            "ERROR": "Erro",
        }
        return mapa.get(verdict, verdict)

    linhas = []
    for item in itens:
        v = item.get("verdict_label") or _label(item.get("verdict", ""))
        cor = _cor(v) if item.get("verdict_label") else _cor(item.get("verdict", ""))
        titulo = item.get("titulo") or f"{item.get('categoria', '')} — {item.get('nome', '')}"
        hora = item.get("quando", "agora")
        dot = "●" if v in ("Falha", "FAIL") else "✓" if v in ("Aprovado", "PASS") else "?"
        linhas.append(
            f"""
            <div class="aegis-result-row">
              <span class="aegis-result-icon" style="color:{cor};">{dot}</span>
              <div class="aegis-result-body">
                <div class="aegis-result-title">{titulo}</div>
                <div class="aegis-result-meta">
                  <span style="color:{cor};font-weight:600;">{v}</span>
                  <span class="aegis-result-time">{hora}</span>
                </div>
              </div>
            </div>
            """
        )
    return f'<div class="aegis-panel aegis-result-list">{"".join(linhas)}</div>'


def faixa_ux_inferior() -> str:
    return f"""
    <div class="aegis-ux-grid">
      <div class="aegis-panel aegis-ux-block">
        <h3 class="aegis-panel-title">Fluxo de Uso (UX)</h3>
        <div class="aegis-flow">
          <div class="aegis-flow-step"><div class="aegis-flow-circle">1</div><strong>Selecionar campanha</strong><span>Perfil e filtros</span></div>
          <div class="aegis-flow-arrow">→</div>
          <div class="aegis-flow-step"><div class="aegis-flow-circle">2</div><strong>Executar testes</strong><span>Campanha no lab</span></div>
          <div class="aegis-flow-arrow">→</div>
          <div class="aegis-flow-step"><div class="aegis-flow-circle">3</div><strong>Ver resultados</strong><span>Evidências por caso</span></div>
          <div class="aegis-flow-arrow">→</div>
          <div class="aegis-flow-step"><div class="aegis-flow-circle">4</div><strong>Gerar relatório</strong><span>JSON e Markdown</span></div>
        </div>
      </div>
      <div class="aegis-panel aegis-ux-block">
        <h3 class="aegis-panel-title">Elementos Visuais da Interface</h3>
        <ul class="aegis-checklist">
          <li>Cores escuras com destaques em verde, azul e roxo.</li>
          <li>Ícones intuitivos e linguagem simples.</li>
          <li>Gráficos que facilitam a análise.</li>
          <li>Tabelas organizadas e filtros de busca.</li>
          <li>Feedbacks visuais para sucesso, aviso e erro.</li>
        </ul>
      </div>
      <div class="aegis-panel aegis-ux-block">
        <h3 class="aegis-panel-title">Exemplo de Interação</h3>
        <p class="aegis-muted">Use a página <strong>Executar Testes</strong> para rodar o laboratório com filtros por categoria e nível de risco.</p>
        <div class="aegis-mini-form">
          <div class="aegis-mini-field">Campanha: perfil da aplicação</div>
          <div class="aegis-mini-chips">
            <span class="aegis-chip">Prompt Injection</span>
            <span class="aegis-chip">Exposição de Dados</span>
            <span class="aegis-chip">Ferramentas e Agentes</span>
            <span class="aegis-chip">Validação E/S</span>
          </div>
          <div class="aegis-mini-cta">Executar Testes</div>
        </div>
      </div>
    </div>
    """


def rodape() -> str:
    return """
    <footer class="aegis-footer">
      <div class="aegis-footer-brand">
        <span class="aegis-footer-logo">🛡</span>
        <span>Aegis AI Lab</span>
      </div>
      <div class="aegis-footer-center">Mais segurança para o futuro da IA</div>
      <div class="aegis-footer-right">
        <span>Projeto de Portfólio</span>
        <span class="aegis-footer-muted">UI (aparência) + UX (experiência) = ferramenta eficiente e agradável de usar.</span>
      </div>
    </footer>
    """
