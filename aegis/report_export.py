"""Exportação de relatórios em Markdown (Etapa 9)."""

from __future__ import annotations

from typing import Any

from aegis.metrics import LIMITACOES_PADRAO, calcular_metricas, comparar_relatorios


def exportar_markdown(relatorio: dict[str, Any]) -> str:
    """Gera relatório técnico legível em Markdown."""
    metricas = calcular_metricas(relatorio)
    camp = relatorio.get("campaign", {})
    lab = relatorio.get("lab", {})
    recs = relatorio.get("recommendations", [])
    limits = relatorio.get("limitations", LIMITACOES_PADRAO)

    linhas = [
        "# Relatório Aegis AI Lab",
        "",
        f"- **Gerado em:** {relatorio.get('generated_at', '?')}",
        f"- **Perfil:** {camp.get('profile', '?')}",
        f"- **Provedor LLM:** {lab.get('llm_provider', '?')}",
        f"- **Modelo Ollama:** {lab.get('ollama_model', '?')}",
        "",
        "## Métricas",
        "",
        f"| Métrica | Valor |",
        f"|---------|------:|",
        f"| Total de casos | {metricas.total} |",
        f"| PASS | {metricas.passed} |",
        f"| FAIL | {metricas.failed} |",
        f"| ERROR | {metricas.errors} |",
        f"| INCONCLUSIVE | {metricas.inconclusive} |",
        f"| Taxa PASS | {metricas.pass_rate:.1%} |",
        f"| Taxa FAIL | {metricas.fail_rate:.1%} |",
        "",
        "### Definições",
        "",
        "- Denominador: total de casos executados.",
        "- INCONCLUSIVE não conta como PASS.",
        "",
        "## Casos",
        "",
    ]

    for item in relatorio.get("results", []):
        linhas.append(f"### {item.get('case_id')} — {item.get('case_name')}")
        linhas.append(f"- **Veredito:** {item.get('verdict')}")
        linhas.append(f"- **Resumo:** {item.get('summary')}")
        linhas.append("")

    linhas.append("## Recomendações")
    linhas.append("")
    for r in recs:
        linhas.append(f"- {r}")

    linhas.append("")
    linhas.append("## Limitações")
    linhas.append("")
    for lim in limits:
        linhas.append(f"- {lim}")

    return "\n".join(linhas)


def exportar_comparacao_markdown(diff: dict[str, Any]) -> str:
    linhas = [
        "# Comparação de campanhas",
        "",
        f"- **Campanha A:** {diff['campaign_a']['profile']} ({diff['campaign_a']['generated_at']})",
        f"- **Campanha B:** {diff['campaign_b']['profile']} ({diff['campaign_b']['generated_at']})",
        f"- **Casos em comum:** {diff['shared_cases']}",
        f"- **Mudanças de veredito:** {diff['verdict_changes']}",
        f"- **FAIL→PASS (melhora):** {diff['improved_fail_to_pass']}",
        f"- **PASS→FAIL (piora):** {diff['worsened_pass_to_fail']}",
        f"- **Δ taxa FAIL:** {diff['fail_rate_delta']}",
        "",
        "## Casos alterados",
        "",
    ]
    for caso in diff.get("cases", []):
        if caso.get("changed"):
            linhas.append(
                f"- **{caso['case_id']}:** {caso['verdict_a']} → {caso['verdict_b']}"
            )
    return "\n".join(linhas)
