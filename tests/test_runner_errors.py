"""Testes do runner — perfil inválido e falhas na aplicação."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from aegis.case_loader import load_all_cases
from aegis.models import Verdict
from aegis.test_runner import TestRunner


def test_perfil_invalido_gera_error(runner: TestRunner) -> None:
    caso = load_all_cases()[0]
    resultado = runner.run_case(caso, "perfil_inexistente")
    assert resultado.verdict.status == Verdict.ERROR
    assert resultado.observation.error_message is not None


def test_excecao_na_app_gera_error(runner: TestRunner) -> None:
    caso = next(c for c in load_all_cases() if c.id == "pi-001")

    class AppQuebrada:
        profile_name = "vulnerable"

        def respond(self, user_message: str):
            raise RuntimeError("falha simulada no backend")

    with patch("aegis.test_runner.criar_assistente", return_value=AppQuebrada()):
        resultado = runner.run_case(caso, "vulnerable")

    assert resultado.verdict.status == Verdict.ERROR
    assert any(ev.code == "execution_error" for ev in resultado.verdict.evidence)
