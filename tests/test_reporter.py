"""Testes do reporter JSON."""

from __future__ import annotations

import json
from pathlib import Path

from aegis.config import Settings
from aegis.reporter import executar_e_salvar_campanha, montar_relatorio, salvar_relatorio
from aegis.test_runner import TestRunner

from tests.constants import LAB_FAKE_SECRET


def _settings() -> Settings:
    return Settings(
        llm_provider="openai",
        openai_api_key=None,
        openai_model="gpt-4o-mini",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="llama3.2",
        llm_timeout_seconds=60.0,
        lab_fake_secret=LAB_FAKE_SECRET,
    )


def test_salvar_relatorio_roundtrip(tmp_path: Path) -> None:
    runner = TestRunner(settings=_settings())
    resultados = runner.run_campaign("protected")
    resumo = runner.summarize(resultados)
    doc = montar_relatorio(resultados, resumo, _settings())
    caminho = salvar_relatorio(doc, tmp_path)
    assert caminho.is_file()
    payload = json.loads(caminho.read_text(encoding="utf-8"))
    assert payload["summary"]["total"] == len(resultados)


def test_executar_e_salvar(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("aegis.reporter.PASTA_RELATORIOS", tmp_path)
    rel, path = executar_e_salvar_campanha(
        "hardened",
        TestRunner(settings=_settings()),
        categories={"prompt_injection"},
    )
    assert path.parent == tmp_path
    assert rel["summary"]["total"] >= 1
