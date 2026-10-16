"""
Carrega casos de teste a partir de arquivos JSON em test_cases/.

Novos casos = novo JSON ou novas entradas no array `cases`, sem alterar o motor principal.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aegis.compliance.models import ComplianceTags
from aegis.models import CriterionType, EvaluationCriterion, Verdict

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
PASTA_CASOS_PADRAO = RAIZ_PROJETO / "test_cases"


@dataclass(frozen=True)
class TestCaseDefinition:
    """Definição estática de um caso (biblioteca JSON)."""

    id: str
    name: str
    risk_category: str
    objective: str
    user_input: str
    expected_behavior: str
    evaluation: EvaluationCriterion
    risk_level: str
    expectations: dict[str, Verdict]
    compliance: ComplianceTags = field(default_factory=ComplianceTags)
    source_file: str = ""


class CaseLoadError(ValueError):
    """Erro de validação ao ler JSON de casos de teste."""


def _parse_verdict(valor: str) -> Verdict:
    try:
        return Verdict(valor.strip().upper())
    except ValueError as exc:
        raise CaseLoadError(f"Veredito esperado inválido: {valor!r}") from exc


def _parse_criterion(data: dict[str, Any]) -> EvaluationCriterion:
    if "type" not in data:
        raise CaseLoadError("Campo evaluation.type é obrigatório.")

    try:
        tipo = CriterionType(data["type"])
    except ValueError as exc:
        raise CaseLoadError(f"Tipo de critério desconhecido: {data['type']!r}") from exc

    forbidden = tuple(data.get("forbidden_substrings") or ())
    required = tuple(data.get("required_substrings") or ())
    case_sensitive = bool(data.get("case_sensitive", False))

    return EvaluationCriterion(
        type=tipo,
        forbidden_substrings=forbidden,
        required_substrings=required,
        case_sensitive=case_sensitive,
    )


def _parse_case(raw: dict[str, Any], source_file: str) -> TestCaseDefinition:
    obrigatorios = (
        "id",
        "name",
        "risk_category",
        "objective",
        "input",
        "expected_behavior",
        "evaluation",
        "risk_level",
    )
    for campo in obrigatorios:
        if campo not in raw:
            raise CaseLoadError(f"Campo obrigatório ausente '{campo}' em caso {raw.get('id', '?')}")

    expectations_raw = raw.get("expectations") or {}
    if not isinstance(expectations_raw, dict):
        raise CaseLoadError(f"expectations deve ser objeto em caso {raw['id']}")

    expectations = {perfil: _parse_verdict(v) for perfil, v in expectations_raw.items()}

    evaluation_raw = raw["evaluation"]
    if not isinstance(evaluation_raw, dict):
        raise CaseLoadError(f"evaluation deve ser objeto em caso {raw['id']}")

    compliance_raw = raw.get("compliance")
    compliance = (
        ComplianceTags.from_raw(compliance_raw)
        if isinstance(compliance_raw, dict)
        else ComplianceTags()
    )

    return TestCaseDefinition(
        id=str(raw["id"]),
        name=str(raw["name"]),
        risk_category=str(raw["risk_category"]),
        objective=str(raw["objective"]),
        user_input=str(raw["input"]),
        expected_behavior=str(raw["expected_behavior"]),
        evaluation=_parse_criterion(evaluation_raw),
        risk_level=str(raw["risk_level"]),
        expectations=expectations,
        compliance=compliance,
        source_file=source_file,
    )


def load_cases_file(path: Path) -> list[TestCaseDefinition]:
    """Lê um arquivo JSON e devolve a lista de casos validados."""
    if not path.is_file():
        raise CaseLoadError(f"Arquivo não encontrado: {path}")

    with path.open(encoding="utf-8") as arquivo:
        payload = json.load(arquivo)

    if not isinstance(payload, dict):
        raise CaseLoadError(f"JSON raiz deve ser objeto: {path}")

    cases_raw = payload.get("cases")
    if not isinstance(cases_raw, list):
        raise CaseLoadError(f"Campo 'cases' deve ser lista em {path}")

    return [_parse_case(item, path.name) for item in cases_raw]


def load_all_cases(directory: Path | None = None) -> list[TestCaseDefinition]:
    """
    Carrega todos os *.json da pasta test_cases (ordem alfabética por arquivo).

    IDs duplicados geram erro para evitar resultados ambíguos nos relatórios.
    """
    pasta = directory or PASTA_CASOS_PADRAO
    if not pasta.is_dir():
        raise CaseLoadError(f"Pasta de casos não encontrada: {pasta}")

    todos: list[TestCaseDefinition] = []
    vistos: set[str] = set()

    for arquivo in sorted(pasta.glob("*.json")):
        for caso in load_cases_file(arquivo):
            if caso.id in vistos:
                raise CaseLoadError(f"ID duplicado na biblioteca: {caso.id}")
            vistos.add(caso.id)
            todos.append(caso)

    return todos
