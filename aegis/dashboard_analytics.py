"""Agregações para gráficos do dashboard."""

from __future__ import annotations

from collections import Counter
from typing import Any

from aegis.reporter import carregar_relatorio, listar_relatorios

_NIVEL_ORDEM = ("critical", "high", "medium", "low")

_LABEL_CATEGORIA = {
    "prompt_injection": "Prompt Injection",
    "data_exposure": "Exposição de Dados",
    "tool_agent": "Ferramentas e Agentes",
    "tools_agents": "Ferramentas e Agentes",
    "input_output_validation": "Validação de Entrada/Saída",
    "outros": "Outros",
}

_LABEL_NIVEL = {
    "critical": "Crítica",
    "high": "Alta",
    "medium": "Média",
    "low": "Baixa",
}


def _vazio() -> dict[str, Any]:
    return {
        "simulado": False,
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "inconclusive": 0,
        "delta_total_pct": None,
        "por_categoria": {},
        "falhas_taxa_severidade": {},
    }


def _metricas_demo() -> dict[str, Any]:
    return {
        "simulado": True,
        "total": 48,
        "passed": 34,
        "failed": 10,
        "errors": 0,
        "inconclusive": 4,
        "delta_total_pct": 12,
        "por_categoria": {
            "Prompt Injection": 15,
            "Exposição de Dados": 11,
            "Ferramentas e Agentes": 8,
            "Validação de Entrada/Saída": 6,
            "Outros": 8,
        },
        "falhas_taxa_severidade": {
            "Crítica": 33.0,
            "Alta": 24.0,
            "Média": 18.0,
            "Baixa": 8.0,
        },
    }


def _label_categoria(chave: str) -> str:
    return _LABEL_CATEGORIA.get(chave, chave.replace("_", " ").title())


def _taxas_falha_por_severidade(resultados: list[dict], total: int) -> dict[str, float]:
    if total <= 0:
        return {}
    contagem: Counter[str] = Counter()
    for item in resultados:
        if item.get("verdict") != "FAIL":
            continue
        nivel = item.get("risk_level", "medium")
        contagem[_LABEL_NIVEL.get(nivel, nivel)] += 1
    # Taxa em relação ao total de testes (mesma leitura do protótipo em %)
    saida: dict[str, float] = {}
    for chave in ("Crítica", "Alta", "Média", "Baixa"):
        saida[chave] = round(100 * contagem.get(chave, 0) / total, 1)
    return saida


def _delta_total_vs_anterior(total_atual: int) -> int | None:
    arquivos = listar_relatorios()
    if len(arquivos) < 2:
        return None
    try:
        anterior = carregar_relatorio(arquivos[1])
        total_ant = anterior.get("summary", {}).get("total", 0) or 0
    except (OSError, ValueError):
        return None
    if total_ant == 0:
        return None
    return int(round(100 * (total_atual - total_ant) / total_ant))


def metricas_de_relatorio(relatorio: dict | None) -> dict[str, Any]:
    if not relatorio:
        return _metricas_demo()

    resumo = relatorio.get("summary", {})
    resultados = relatorio.get("results", [])
    total = resumo.get("total", 0) or len(resultados)

    if total == 0:
        return _metricas_demo()

    por_cat: Counter[str] = Counter()
    for item in resultados:
        por_cat[_label_categoria(item.get("risk_category", "outros"))] += 1

    return {
        "simulado": False,
        "total": total,
        "passed": resumo.get("passed", 0),
        "failed": resumo.get("failed", 0),
        "errors": resumo.get("errors", 0),
        "inconclusive": resumo.get("inconclusive", 0),
        "delta_total_pct": _delta_total_vs_anterior(total),
        "por_categoria": dict(por_cat),
        "falhas_taxa_severidade": _taxas_falha_por_severidade(resultados, total),
    }


def campanhas_demo() -> list[dict[str, Any]]:
    return [
        {
            "nome": "Campanha 01 — Modelo Local",
            "data": "2026-10-10",
            "testes": 48,
            "pass_pct": 71,
            "status": "Concluída",
            "simulado": True,
        },
        {
            "nome": "Campanha 02 — Com Defesas",
            "data": "2026-10-12",
            "testes": 48,
            "pass_pct": 88,
            "status": "Concluída",
            "simulado": True,
        },
        {
            "nome": "Campanha 03 — Testes Específicos",
            "data": "2026-10-14",
            "testes": 24,
            "pass_pct": 62,
            "status": "Concluída",
            "simulado": True,
        },
        {
            "nome": "Campanha 04 — Nova Versão",
            "data": "2026-10-15",
            "testes": 48,
            "pass_pct": 79,
            "status": "Concluída",
            "simulado": True,
        },
    ]


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
                "simulado": False,
            }
        )
    return linhas


def campanhas_para_dashboard() -> tuple[list[dict[str, Any]], bool]:
    reais = listar_campanhas_resumo()
    if reais:
        return reais[:4], False
    return campanhas_demo(), True


def resultados_demo() -> list[dict[str, Any]]:
    return [
        {
            "titulo": "Prompt Injection — Ignorar instruções",
            "verdict_label": "Falha",
            "quando": "há 12 min",
            "simulado": True,
        },
        {
            "titulo": "Exposição de Dados — Segredo de teste",
            "verdict_label": "Aprovado",
            "quando": "há 28 min",
            "simulado": True,
        },
        {
            "titulo": "Ferramentas — Acesso indevido",
            "verdict_label": "Inconclusivo",
            "quando": "há 1 h",
            "simulado": True,
        },
        {
            "titulo": "Validação — Entrada maliciosa",
            "verdict_label": "Aprovado",
            "quando": "há 2 h",
            "simulado": True,
        },
        {
            "titulo": "Prompt Injection — Conteúdo externo",
            "verdict_label": "Falha",
            "quando": "há 3 h",
            "simulado": True,
        },
    ]


def ultimos_resultados(relatorio: dict | None, limite: int = 6) -> list[dict[str, Any]]:
    if not relatorio:
        return resultados_demo()
    itens = relatorio.get("results", [])[-limite:]
    if not itens:
        return resultados_demo()
    itens = list(reversed(itens))
    saida = []
    for item in itens:
        cat = _label_categoria(item.get("risk_category", "outros"))
        saida.append(
            {
                "id": item.get("case_id"),
                "nome": item.get("case_name"),
                "categoria": cat,
                "verdict": item.get("verdict"),
                "quando": "última execução",
                "simulado": False,
            }
        )
    return saida


def carregar_ultimo_relatorio_automatico() -> tuple[dict | None, str | None]:
    arquivos = listar_relatorios()
    if not arquivos:
        return None, None
    caminho = arquivos[0]
    return carregar_relatorio(caminho), str(caminho)
