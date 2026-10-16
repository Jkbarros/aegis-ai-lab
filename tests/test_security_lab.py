"""Etapa 10 — segurança do próprio laboratório."""

from __future__ import annotations

import json
from pathlib import Path

from aegis.config import Settings
from aegis.reporter import montar_relatorio, salvar_relatorio
from aegis.security.report_safety import (
    encontrar_violacoes,
    relatorio_seguro_para_export,
    sanitize_report_document,
)
from aegis.test_runner import TestRunner

from tests.constants import LAB_FAKE_SECRET

_FAKE_OPENAI = "sk-fakekey123456789012345678901234567890"


def _settings() -> Settings:
    return Settings(
        llm_provider="openai",
        openai_api_key=_FAKE_OPENAI,
        openai_model="gpt-4o-mini",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="llama3.2",
        llm_timeout_seconds=60.0,
        lab_fake_secret=LAB_FAKE_SECRET,
    )


def test_sanitize_remove_lab_secret_and_api_key() -> None:
    cfg = _settings()
    bruto = {
        "lab": {"llm_provider": "openai"},
        "results": [{"response_text": f"vazou {LAB_FAKE_SECRET} e {_FAKE_OPENAI}"}],
    }
    limpo = sanitize_report_document(bruto, cfg)
    texto = json.dumps(limpo)
    assert LAB_FAKE_SECRET not in texto
    assert _FAKE_OPENAI not in texto
    assert "[REDACTED_LAB_SECRET]" in texto
    assert limpo["security"]["sanitized_for_export"] is True


def test_vulnerable_campanha_salva_sem_segredo_bruto(tmp_path: Path) -> None:
    cfg = _settings()
    runner = TestRunner(settings=cfg)
    resultados = runner.run_campaign("vulnerable")
    doc = montar_relatorio(resultados, runner.summarize(resultados), cfg)
    caminho = salvar_relatorio(doc, tmp_path, settings=cfg)
    salvo = json.loads(caminho.read_text(encoding="utf-8"))
    assert LAB_FAKE_SECRET not in json.dumps(salvo)
    assert not encontrar_violacoes(salvo, cfg)


def test_montar_relatorio_nao_inclui_api_key_no_lab() -> None:
    cfg = _settings()
    runner = TestRunner(settings=cfg)
    res = runner.run_campaign("protected")
    doc = montar_relatorio(res, runner.summarize(res), cfg)
    assert "openai_api_key" not in json.dumps(doc.get("lab", {}))


def test_relatorio_seguro_para_export_apos_sanitize() -> None:
    cfg = _settings()
    doc = {"results": [{"summary": f"key {_FAKE_OPENAI}"}]}
    assert relatorio_seguro_para_export(doc, cfg)
