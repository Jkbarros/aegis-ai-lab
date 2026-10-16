"""Testes de métricas e comparação — Etapa 9."""

from __future__ import annotations

from aegis.config import Settings
from aegis.metrics import calcular_metricas, comparar_relatorios
from aegis.reporter import montar_relatorio, salvar_relatorio
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


def test_taxas_usam_total_como_denominador() -> None:
    runner = TestRunner(settings=_settings())
    vuln = runner.run_campaign("vulnerable")
    doc = montar_relatorio(vuln, runner.summarize(vuln), _settings())
    m = calcular_metricas(doc)
    assert m.total == len(vuln)
    assert abs(m.pass_rate + m.fail_rate + m.error_rate + m.inconclusive_rate - 1.0) < 0.001


def test_relatorio_tem_metricas_e_recomendacoes() -> None:
    runner = TestRunner(settings=_settings())
    res = runner.run_campaign("protected")
    doc = montar_relatorio(res, runner.summarize(res), _settings())
    assert doc["schema_version"] == "1.1"
    assert "metrics" in doc
    assert doc["metrics"]["rates"]["pass_rate"] == 1.0
    assert doc["recommendations"]
    assert doc["limitations"]


def test_comparar_vulnerable_vs_hardened() -> None:
    runner = TestRunner(settings=_settings())
    a = montar_relatorio(
        runner.run_campaign("vulnerable"),
        runner.summarize(runner.run_campaign("vulnerable")),
        _settings(),
    )
    b = montar_relatorio(
        runner.run_campaign("hardened"),
        runner.summarize(runner.run_campaign("hardened")),
        _settings(),
    )
    diff = comparar_relatorios(a, b)
    assert diff["shared_cases"] == 8
    assert diff["improved_fail_to_pass"] >= 1


def test_salvar_gera_markdown(tmp_path) -> None:
    runner = TestRunner(settings=_settings())
    res = runner.run_campaign("protected")
    doc = montar_relatorio(res, runner.summarize(res), _settings())
    path = salvar_relatorio(doc, tmp_path)
    assert path.with_suffix(".md").is_file()
