"""
Métricas formais do laboratório (Etapa 9).

Todas as taxas usam o mesmo denominador: total de casos executados na campanha.
INCONCLUSIVE não é contado como PASS nem como FAIL.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CampaignMetrics:
    """Métricas derivadas de um relatório já serializado."""

    total: int
    passed: int
    failed: int
    errors: int
    inconclusive: int
    pass_rate: float
    fail_rate: float
    error_rate: float
    inconclusive_rate: float
    expectation_checks: int
    expectation_matches: int
    expectation_match_rate: float | None
    by_category: dict[str, dict[str, int]]
    by_risk_level: dict[str, dict[str, int]]


def calcular_metricas(relatorio: dict[str, Any]) -> CampaignMetrics:
    resultados = relatorio.get("results", [])
    total = len(resultados)
    if total == 0:
        return CampaignMetrics(
            total=0,
            passed=0,
            failed=0,
            errors=0,
            inconclusive=0,
            pass_rate=0.0,
            fail_rate=0.0,
            error_rate=0.0,
            inconclusive_rate=0.0,
            expectation_checks=0,
            expectation_matches=0,
            expectation_match_rate=None,
            by_category={},
            by_risk_level={},
        )

    passed = sum(1 for r in resultados if r.get("verdict") == "PASS")
    failed = sum(1 for r in resultados if r.get("verdict") == "FAIL")
    errors = sum(1 for r in resultados if r.get("verdict") == "ERROR")
    inconclusive = sum(1 for r in resultados if r.get("verdict") == "INCONCLUSIVE")

    checks = [r for r in resultados if r.get("expected_verdict") is not None]
    matches = sum(1 for r in checks if r.get("expectation_met") is True)

    por_cat: dict[str, dict[str, int]] = {}
    por_nivel: dict[str, dict[str, int]] = {}

    for item in resultados:
        cat = item.get("risk_category", "outros")
        nivel = item.get("risk_level", "unknown")
        ver = item.get("verdict", "ERROR")
        por_cat.setdefault(cat, {"PASS": 0, "FAIL": 0, "ERROR": 0, "INCONCLUSIVE": 0})
        por_nivel.setdefault(nivel, {"PASS": 0, "FAIL": 0, "ERROR": 0, "INCONCLUSIVE": 0})
        if ver in por_cat[cat]:
            por_cat[cat][ver] += 1
        if ver in por_nivel[nivel]:
            por_nivel[nivel][ver] += 1

    return CampaignMetrics(
        total=total,
        passed=passed,
        failed=failed,
        errors=errors,
        inconclusive=inconclusive,
        pass_rate=passed / total,
        fail_rate=failed / total,
        error_rate=errors / total,
        inconclusive_rate=inconclusive / total,
        expectation_checks=len(checks),
        expectation_matches=matches,
        expectation_match_rate=(matches / len(checks)) if checks else None,
        by_category=por_cat,
        by_risk_level=por_nivel,
    )


def metricas_para_dict(metricas: CampaignMetrics) -> dict[str, Any]:
    return {
        "definitions": {
            "denominator": "total de casos executados na campanha",
            "pass_rate": "PASS / total (INCONCLUSIVE não entra como aprovado)",
            "fail_rate": "FAIL / total",
            "error_rate": "ERROR / total",
            "inconclusive_rate": "INCONCLUSIVE / total",
            "expectation_match_rate": "casos com expectation_met=True / casos com expected_verdict definido no JSON",
        },
        "counts": {
            "total": metricas.total,
            "passed": metricas.passed,
            "failed": metricas.failed,
            "errors": metricas.errors,
            "inconclusive": metricas.inconclusive,
        },
        "rates": {
            "pass_rate": round(metricas.pass_rate, 4),
            "fail_rate": round(metricas.fail_rate, 4),
            "error_rate": round(metricas.error_rate, 4),
            "inconclusive_rate": round(metricas.inconclusive_rate, 4),
            "expectation_match_rate": (
                round(metricas.expectation_match_rate, 4)
                if metricas.expectation_match_rate is not None
                else None
            ),
        },
        "expectation_checks": metricas.expectation_checks,
        "expectation_matches": metricas.expectation_matches,
        "by_category": metricas.by_category,
        "by_risk_level": metricas.by_risk_level,
    }


def comparar_relatorios(
    base: dict[str, Any],
    comparacao: dict[str, Any],
) -> dict[str, Any]:
    """
    Compara duas campanhas pelo case_id.

    Útil para contrastar perfis (ex.: vulnerable vs hardened) ou execuções no tempo.
    """
    mapa_a = {r["case_id"]: r for r in base.get("results", [])}
    mapa_b = {r["case_id"]: r for r in comparacao.get("results", [])}
    ids = sorted(set(mapa_a) & set(mapa_b))

    linhas = []
    mudou_veredito = 0
    melhorou = 0
    piorou = 0

    for case_id in ids:
        a = mapa_a[case_id]
        b = mapa_b[case_id]
        va = a.get("verdict")
        vb = b.get("verdict")
        if va != vb:
            mudou_veredito += 1
            if va == "FAIL" and vb == "PASS":
                melhorou += 1
            elif va == "PASS" and vb == "FAIL":
                piorou += 1
        linhas.append(
            {
                "case_id": case_id,
                "case_name": a.get("case_name"),
                "verdict_a": va,
                "verdict_b": vb,
                "changed": va != vb,
            }
        )

    m_a = calcular_metricas(base)
    m_b = calcular_metricas(comparacao)

    return {
        "campaign_a": {
            "profile": base.get("campaign", {}).get("profile"),
            "generated_at": base.get("generated_at"),
            "fail_rate": round(m_a.fail_rate, 4),
        },
        "campaign_b": {
            "profile": comparacao.get("campaign", {}).get("profile"),
            "generated_at": comparacao.get("generated_at"),
            "fail_rate": round(m_b.fail_rate, 4),
        },
        "shared_cases": len(ids),
        "verdict_changes": mudou_veredito,
        "improved_fail_to_pass": melhorou,
        "worsened_pass_to_fail": piorou,
        "fail_rate_delta": round(m_b.fail_rate - m_a.fail_rate, 4),
        "cases": linhas,
    }


def gerar_recomendacoes(relatorio: dict[str, Any]) -> list[str]:
    """Sugestões didáticas baseadas em falhas observadas (não substitui revisão humana)."""
    metricas = calcular_metricas(relatorio)
    dicas: list[str] = []

    if metricas.failed > 0:
        dicas.append(
            "Revise os casos FAIL e as evidências: confirme se há vazamento real ou falso positivo."
        )
    if metricas.inconclusive > 0:
        dicas.append(
            "Trate casos INCONCLUSIVE com revisão manual antes de usar a taxa de aprovação em decisões."
        )
    for cat, contagem in metricas.by_category.items():
        if contagem.get("FAIL", 0) > 0:
            dicas.append(
                f"Priorize mitigação em '{cat}' ({contagem['FAIL']} FAIL nesta campanha)."
            )
    if metricas.expectation_match_rate is not None and metricas.expectation_match_rate < 1.0:
        dicas.append(
            "Expectativas do JSON não bateram em todos os casos — alinhe perfil da app ou atualize o caso de teste."
        )
    if not dicas:
        dicas.append(
            "Nenhuma falha registrada nesta campanha; mantenha testes de regressão ao alterar prompts ou controles."
        )
    return dicas


LIMITACOES_PADRAO = [
    "Heurísticas do avaliador não cobrem todos os vetores de prompt injection.",
    "Apps com LLM real podem variar entre execuções; resultados simulados são mais reproduzíveis.",
    "Taxas refletem apenas os casos executados nesta campanha (filtros reduzem o escopo).",
    "INCONCLUSIVE exige julgamento humano e não deve ser tratado como aprovação.",
]
