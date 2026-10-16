"""
Cobertura de frameworks a partir de resultados de campanha.

Os mapeamentos são orientativos para estudo e portfólio — não substituem
assessment formal contra OWASP, MITRE ou NIST.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aegis.case_loader import TestCaseDefinition, load_all_cases
from aegis.compliance.models import FRAMEWORK_KEYS, ComplianceTags

CATALOGO_PATH = Path(__file__).resolve().parent / "framework_catalog.json"

_DEFAULTS_POR_CATEGORIA: dict[str, ComplianceTags] = {
    "prompt_injection": ComplianceTags(
        owasp_llm=("LLM01",),
        mitre_attack=("T1566",),
        mitre_atlas=("AML.T0051",),
        nist_csf=("DE.CM", "PR.DS"),
    ),
    "data_exposure": ComplianceTags(
        owasp_llm=("LLM02",),
        mitre_attack=("T1530", "T1213"),
        mitre_atlas=("AML.T0024",),
        nist_csf=("PR.DS", "RS.MA"),
    ),
}


def carregar_catalogo() -> dict[str, Any]:
    if not CATALOGO_PATH.is_file():
        return {"frameworks": {}, "disclaimer": ""}
    with CATALOGO_PATH.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def _tags_efetivas(item: dict[str, Any], caso: TestCaseDefinition | None) -> dict[str, list[str]]:
    raw = item.get("compliance")
    if isinstance(raw, dict) and any(raw.get(fw) for fw in FRAMEWORK_KEYS):
        return {fw: list(raw.get(fw) or []) for fw in FRAMEWORK_KEYS}
    if caso:
        return compliance_do_caso(caso).to_dict()
    return {fw: [] for fw in FRAMEWORK_KEYS}


def compliance_do_caso(caso: TestCaseDefinition) -> ComplianceTags:
    if caso.compliance and any(caso.compliance.to_dict().values()):
        return caso.compliance
    return _DEFAULTS_POR_CATEGORIA.get(
        caso.risk_category,
        ComplianceTags(nist_csf=("GV.OC",)),
    )


def _indice_casos() -> dict[str, TestCaseDefinition]:
    return {c.id: c for c in load_all_cases()}


def cobertura_por_framework(relatorio: dict[str, Any]) -> dict[str, Any]:
    """
    Agrega PASS/FAIL por ID de controle/técnica em cada framework.

    Cada caso pode exercitar várias tags; o veredito do caso conta para todas.
    """
    catalogo = carregar_catalogo()
    indice = _indice_casos()
    por_fw: dict[str, dict[str, dict[str, int]]] = {k: {} for k in FRAMEWORK_KEYS}

    for item in relatorio.get("results", []):
        case_id = item.get("case_id", "")
        caso = indice.get(case_id)
        tags = _tags_efetivas(item, caso)
        veredito = item.get("verdict", "ERROR")
        for fw in FRAMEWORK_KEYS:
            for tag_id in tags.get(fw, []):
                slot = por_fw[fw].setdefault(
                    tag_id,
                    {"tested": 0, "pass": 0, "fail": 0, "other": 0},
                )
                slot["tested"] += 1
                if veredito == "PASS":
                    slot["pass"] += 1
                elif veredito == "FAIL":
                    slot["fail"] += 1
                else:
                    slot["other"] += 1

    frameworks_meta = catalogo.get("frameworks", {})
    resumo_frameworks: dict[str, Any] = {}

    for fw, controles in por_fw.items():
        meta = frameworks_meta.get(fw, {})
        itens = []
        for ctrl_id, contagem in sorted(controles.items()):
            definicao = (meta.get("items") or {}).get(ctrl_id, {})
            itens.append(
                {
                    "id": ctrl_id,
                    "name": definicao.get("name", ctrl_id),
                    "tested": contagem["tested"],
                    "pass": contagem["pass"],
                    "fail": contagem["fail"],
                    "other": contagem["other"],
                }
            )
        resumo_frameworks[fw] = {
            "title": meta.get("title", fw),
            "reference": meta.get("reference", ""),
            "controls": itens,
        }

    return {
        "disclaimer": catalogo.get(
            "disclaimer",
            "Mapeamento didático; não é certificação oficial.",
        ),
        "frameworks": resumo_frameworks,
    }


def anexar_compliance_ao_relatorio(relatorio: dict[str, Any]) -> dict[str, Any]:
    """Enriquece resultados com tags e bloco `compliance_coverage` no relatório."""
    indice = _indice_casos()
    resultados = []
    for item in relatorio.get("results", []):
        copia = dict(item)
        caso = indice.get(copia.get("case_id", ""))
        if caso and "compliance" not in copia:
            copia["compliance"] = compliance_do_caso(caso).to_dict()
        resultados.append(copia)
    relatorio = dict(relatorio)
    relatorio["results"] = resultados
    relatorio["compliance_coverage"] = cobertura_por_framework(relatorio)
    relatorio["compliance_catalog"] = {
        "path": "aegis/compliance/framework_catalog.json",
        "frameworks": list(FRAMEWORK_KEYS),
    }
    return relatorio


def biblioteca_compliance_markdown() -> str:
    """Tabela resumida da biblioteca de casos x frameworks."""
    catalogo = carregar_catalogo()
    linhas = ["| Caso | OWASP LLM | MITRE ATT&CK | MITRE ATLAS | NIST CSF |", "|------|-----------|--------------|-------------|----------|"]
    for caso in load_all_cases():
        tags = compliance_do_caso(caso)
        d = tags.to_dict()
        linhas.append(
            f"| {caso.id} | {', '.join(d['owasp_llm']) or '—'} | "
            f"{', '.join(d['mitre_attack']) or '—'} | "
            f"{', '.join(d['mitre_atlas']) or '—'} | "
            f"{', '.join(d['nist_csf']) or '—'} |"
        )
    return "\n".join(linhas)
