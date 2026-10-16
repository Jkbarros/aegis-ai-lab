"""Testes do carregador JSON — entradas válidas e inválidas."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aegis.case_loader import CaseLoadError, load_all_cases, load_cases_file


def test_arquivo_inexistente() -> None:
    with pytest.raises(CaseLoadError, match="não encontrado"):
        load_cases_file(Path("test_cases/nao_existe.json"))


def test_json_sem_lista_cases(tmp_path: Path) -> None:
    arquivo = tmp_path / "bad.json"
    arquivo.write_text('{"schema_version": "1.0"}', encoding="utf-8")
    with pytest.raises(CaseLoadError, match="cases"):
        load_cases_file(arquivo)


def test_criterio_desconhecido(tmp_path: Path) -> None:
    payload = {
        "cases": [
            {
                "id": "x-1",
                "name": "n",
                "risk_category": "c",
                "objective": "o",
                "input": "i",
                "expected_behavior": "e",
                "evaluation": {"type": "criterio_inventado"},
                "risk_level": "low",
            }
        ]
    }
    arquivo = tmp_path / "bad.json"
    arquivo.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(CaseLoadError, match="desconhecido"):
        load_cases_file(arquivo)


def test_expectations_veredito_invalido(tmp_path: Path) -> None:
    payload = {
        "cases": [
            {
                "id": "x-2",
                "name": "n",
                "risk_category": "c",
                "objective": "o",
                "input": "i",
                "expected_behavior": "e",
                "evaluation": {"type": "must_not_leak_secret"},
                "risk_level": "low",
                "expectations": {"protected": "MAYBE"},
            }
        ]
    }
    arquivo = tmp_path / "bad.json"
    arquivo.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(CaseLoadError, match="inválido"):
        load_cases_file(arquivo)


@pytest.mark.integration
def test_biblioteca_oficial_tem_oito_casos() -> None:
    casos = load_all_cases()
    assert len(casos) >= 8
