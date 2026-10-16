"""
Geração de relatórios e persistência em JSON (Etapas 8–9).

Os arquivos ficam em reports/ (ignorados pelo Git exceto a pasta).
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from aegis.config import Settings, get_settings
from aegis.security.report_safety import sanitize_report_document
from aegis.metrics import (
    LIMITACOES_PADRAO,
    calcular_metricas,
    comparar_relatorios,
    gerar_recomendacoes,
    metricas_para_dict,
)
from aegis.report_export import exportar_markdown
from aegis.test_runner import CampaignSummary, CaseExecutionResult, TestRunner

RAIZ = Path(__file__).resolve().parents[1]
PASTA_RELATORIOS = RAIZ / "reports"


def _agora_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resultado_para_dict(resultado: CaseExecutionResult) -> dict[str, Any]:
    """Serializa um resultado de caso para JSON (sem objetos não serializáveis)."""
    caso = resultado.case
    veredito = resultado.verdict
    obs = resultado.observation

    return {
        "case_id": caso.id,
        "case_name": caso.name,
        "risk_category": caso.risk_category,
        "risk_level": caso.risk_level,
        "objective": caso.objective,
        "user_input": obs.user_input,
        "profile": resultado.profile,
        "response_text": obs.response_text,
        "error_message": obs.error_message,
        "verdict": veredito.status.value,
        "criterion": veredito.criterion.value,
        "summary": veredito.summary,
        "expected_verdict": (
            resultado.expected_verdict.value if resultado.expected_verdict else None
        ),
        "expectation_met": resultado.expectation_met,
        "evidence": [
            {"code": e.code, "message": e.message, "snippet": e.snippet}
            for e in veredito.evidence
        ],
    }


def resumo_para_dict(resumo: CampaignSummary) -> dict[str, Any]:
    return asdict(resumo)


def montar_relatorio(
    resultados: list[CaseExecutionResult],
    resumo: CampaignSummary,
    settings: Settings | None = None,
    *,
    notas: str = "",
) -> dict[str, Any]:
    """Monta o documento completo da campanha (schema 1.1 com métricas)."""
    cfg = settings or get_settings()
    doc: dict[str, Any] = {
        "schema_version": "1.1",
        "generated_at": _agora_iso(),
        "lab": {
            "llm_provider": cfg.llm_provider,
            "ollama_model": cfg.ollama_model,
            "openai_model": cfg.openai_model,
        },
        "campaign": {
            "profile": resumo.profile,
            "notes": notas,
        },
        "summary": resumo_para_dict(resumo),
        "results": [resultado_para_dict(r) for r in resultados],
    }
    doc["metrics"] = metricas_para_dict(calcular_metricas(doc))
    doc["recommendations"] = gerar_recomendacoes(doc)
    doc["limitations"] = list(LIMITACOES_PADRAO)
    return doc


def salvar_relatorio(
    relatorio: dict[str, Any],
    pasta: Path | None = None,
    *,
    settings: Settings | None = None,
) -> Path:
    """Grava JSON sanitizado em reports/ e devolve o caminho do arquivo."""
    destino = pasta or PASTA_RELATORIOS
    destino.mkdir(parents=True, exist_ok=True)

    cfg = settings or get_settings()
    seguro = sanitize_report_document(relatorio, cfg)

    perfil = seguro.get("campaign", {}).get("profile", "unknown")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    nome = f"campaign_{timestamp}_{perfil}.json"
    caminho = destino / nome

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(seguro, arquivo, ensure_ascii=False, indent=2)

    md_path = caminho.with_suffix(".md")
    md_path.write_text(exportar_markdown(seguro), encoding="utf-8")

    return caminho


def comparar_campanhas_salvas(caminho_a: Path, caminho_b: Path) -> dict[str, Any]:
    """Carrega dois JSON de reports/ e devolve comparação estruturada."""
    return comparar_relatorios(carregar_relatorio(caminho_a), carregar_relatorio(caminho_b))


def listar_relatorios(pasta: Path | None = None) -> list[Path]:
    """Lista relatórios JSON salvos (mais recentes primeiro)."""
    destino = pasta or PASTA_RELATORIOS
    if not destino.is_dir():
        return []
    arquivos = sorted(destino.glob("campaign_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return arquivos


def carregar_relatorio(caminho: Path) -> dict[str, Any]:
    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def executar_e_salvar_campanha(
    profile: str,
    runner: TestRunner | None = None,
    *,
    categories: set[str] | None = None,
    risk_levels: set[str] | None = None,
    case_ids: set[str] | None = None,
    notas: str = "",
) -> tuple[dict[str, Any], Path]:
    """
    Executa campanha com filtros opcionais, salva relatório e retorna (dict, path).

    Filtros de categoria/nível/ID são aplicados antes da execução.
    """
    from aegis.case_loader import load_all_cases

    exec_runner = runner or TestRunner()
    casos = load_all_cases()
    if categories:
        casos = [c for c in casos if c.risk_category in categories]
    if risk_levels:
        casos = [c for c in casos if c.risk_level in risk_levels]
    if case_ids:
        casos = [c for c in casos if c.id in case_ids]

    resultados = exec_runner.run_cases(casos, profile)
    resumo = exec_runner.summarize(resultados)
    cfg = get_settings()
    relatorio = montar_relatorio(resultados, resumo, cfg, notas=notas)
    caminho = salvar_relatorio(relatorio, settings=cfg)
    # Estado da UI e downloads usam a versão sanitizada (igual ao arquivo em disco).
    relatorio_export = sanitize_report_document(relatorio, cfg)
    return relatorio_export, caminho
