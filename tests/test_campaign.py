"""Testes do carregador JSON e do executor de campanha — Etapa 4."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aegis.case_loader import CaseLoadError, load_all_cases
from aegis.models import Verdict
from aegis.test_runner import TestRunner


def test_carrega_biblioteca_padrao() -> None:
    casos = load_all_cases()
    assert len(casos) >= 8
    ids = {c.id for c in casos}
    assert "pi-002" in ids
    assert "de-001" in ids


def test_id_duplicado_rejeitado(tmp_path: Path) -> None:
    conteudo = {
        "schema_version": "1.0",
        "cases": [
            {
                "id": "dup-1",
                "name": "a",
                "risk_category": "x",
                "objective": "o",
                "input": "i",
                "expected_behavior": "e",
                "evaluation": {"type": "must_not_leak_secret"},
                "risk_level": "low",
                "expectations": {"protected": "PASS"},
            }
        ],
    }
    (tmp_path / "a.json").write_text(json.dumps(conteudo), encoding="utf-8")
    (tmp_path / "b.json").write_text(json.dumps(conteudo), encoding="utf-8")
    with pytest.raises(CaseLoadError, match="duplicado"):
        load_all_cases(tmp_path)


@pytest.mark.integration
def test_campanha_protected_alinha_expectations(runner: TestRunner) -> None:
    resultados = runner.run_campaign("protected")
    assert all(r.expectation_met is not False for r in resultados if r.expected_verdict)


def test_campanha_vulnerable_pi002_fail(runner: TestRunner) -> None:
    casos = [c for c in load_all_cases() if c.id == "pi-002"]
    resultado = runner.run_case(casos[0], "vulnerable")
    assert resultado.verdict.status == Verdict.FAIL
    assert resultado.expectation_met is True


def test_filtrar_categoria(runner: TestRunner) -> None:
    resultados = runner.run_campaign("protected", categories={"data_exposure"})
    assert resultados
    assert all(r.case.risk_category == "data_exposure" for r in resultados)
