"""Agregações para gráficos do dashboard."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from aegis.reporter import carregar_relatorio, listar_relatorios

_NIVEL_ORDEM = ("critical", "high", "medium", "low")


def _vazio() -> dict[str, Any]:
    return {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "inconclusive": 0,
        "por_categoria": {},
        "falhas_por_nivel": {},
    }


def metricas_de_relatorio(relatorio: dict | None) -> dict[str, Any]:
    if not relatorio:
        return _vazio()

    resumo = relatorio.get("summary", {})
    resultados = relatorio.get("results", [])

    por_cat: Counter[str] = Counter()
    falhas_nivel: Counter[str] = Counter()

    for item in resultados:
        cat = item.get("risk_category", "outros")
        por_cat[cat] += 1
        if item.get("verdict") == "FAIL":
            nivel = item.get("risk_level", "medium")
            falhas_nivel[nivel] += 1

    return {
        "total": resumo.get("total", 0),
        "passed": resumo.get("passed", 0),
        "failed": resumo.get("failed", 0),
        "errors": resumo.get("errors", 0),
        "inconclusive": resumo.get("inconclusive", 0),
        "por_categoria": dict(por_cat),
        "falhas_por_nivel": dict(falhas_nivel),
    }


def listar_campanhas_resumo(limite: int = 8) -> list[dict[str, Any]]:
    linhas: list[dict[str, Any]] = []
    for caminho in listar_relatorios()[:limite]:
        try:
            doc = carregar_relatorio(caminho)
        except (OSError, ValueError):
            continue
        s = doc.get("summary", {})
        total = s.get("total", 0) or 1
        pass_pct = int(100 * s.get("passed", 0) / total)
        linhas.append(
            {
                "nome": caminho.stem.replace("campaign_", "Campanha "),
                "arquivo": caminho.name,
                "data": doc.get("generated_at", "-")[:10],
                "testes": s.get("total", 0),
                "pass_pct": pass_pct,
                "perfil": doc.get("campaign", {}).get("profile", "?"),
                "status": "Concluída",
            }
        )
    return linhas


def ultimos_resultados(relatorio: dict | None, limite: int = 6) -> list[dict[str, Any]]:
    if not relatorio:
        return []
    itens = relatorio.get("results", [])[-limite:]
    itens.reverse()
    saida = []
    for item in itens:
        saida.append(
            {
                "id": item.get("case_id"),
                "nome": item.get("case_name"),
                "verdict": item.get("verdict"),
                "categoria": item.get("risk_category"),
            }
        )
    return saida


def carregar_ultimo_relatorio_automatico() -> tuple[dict | None, str | None]:
    arquivos = listar_relatorios()
    if not arquivos:
        return None, None
    caminho = arquivos[0]
    return carregar_relatorio(caminho), str(caminho)
