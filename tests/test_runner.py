"""Testes do carregador JSON e do executor de campanha — Etapa 4."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.case_loader import CaseLoadError, load_all_cases, load_cases_file
from aegis.config import Settings
from aegis.models import Verdict
from aegis.test_runner import TestRunner

SEGREDO = "LAB-FAKE-SECRET-FOR-RUNNER-TESTS"


def _settings() -> Settings:
    return Settings(
        llm_provider="openai",
        openai_api_key=None,
        openai_model="gpt-4o-mini",
        llm_timeout_seconds=60.0,
        lab_fake_secret=SEGREDO,
    )


def test_carrega_biblioteca_padrao() -> None:
    casos = load_all_cases()
    assert len(casos) >= 8
    ids = {c.id for c in casos}
    assert "pi-002" in ids
    assert "de-001" in ids


def test_id_duplicado_rejeitado() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp)
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
        (pasta / "a.json").write_text(json.dumps(conteudo), encoding="utf-8")
        (pasta / "b.json").write_text(json.dumps(conteudo), encoding="utf-8")
        try:
            load_all_cases(pasta)
            raise AssertionError("deveria falhar com ID duplicado")
        except CaseLoadError:
            pass


def test_campanha_protected_alinha_expectations() -> None:
    runner = TestRunner(settings=_settings())
    resultados = runner.run_campaign("protected")
    assert all(r.expectation_met is not False for r in resultados if r.expected_verdict)


def test_campanha_vulnerable_pi002_fail() -> None:
    runner = TestRunner(settings=_settings())
    casos = [c for c in load_all_cases() if c.id == "pi-002"]
    resultado = runner.run_case(casos[0], "vulnerable")
    assert resultado.verdict.status == Verdict.FAIL
    assert resultado.expectation_met is True


def test_filtrar_categoria() -> None:
    runner = TestRunner(settings=_settings())
    resultados = runner.run_campaign("protected", categories={"data_exposure"})
    assert resultados
    assert all(r.case.risk_category == "data_exposure" for r in resultados)


if __name__ == "__main__":
    test_carrega_biblioteca_padrao()
    test_id_duplicado_rejeitado()
    test_campanha_protected_alinha_expectations()
    test_campanha_vulnerable_pi002_fail()
    test_filtrar_categoria()
    print("OK: tests/test_runner.py passou.")
