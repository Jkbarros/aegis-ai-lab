"""Testes de mapeamento OWASP / MITRE / NIST."""

from __future__ import annotations

from aegis.case_loader import load_all_cases
from aegis.compliance.coverage import carregar_catalogo, cobertura_por_framework, compliance_do_caso
from aegis.config import Settings
from aegis.reporter import montar_relatorio
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


def test_catalogo_tem_quatro_frameworks() -> None:
    cat = carregar_catalogo()
    fws = cat.get("frameworks", {})
    assert "owasp_llm" in fws
    assert "mitre_attack" in fws
    assert "mitre_atlas" in fws
    assert "nist_csf" in fws


def test_pi002_mapeia_owasp_llm01() -> None:
    caso = next(c for c in load_all_cases() if c.id == "pi-002")
    tags = compliance_do_caso(caso)
    assert "LLM01" in tags.owasp_llm


def test_relatorio_inclui_compliance_coverage() -> None:
    runner = TestRunner(settings=_settings())
    res = runner.run_campaign("hardened")
    doc = montar_relatorio(res, runner.summarize(res), _settings())
    assert "compliance_coverage" in doc
    owasp = doc["compliance_coverage"]["frameworks"]["owasp_llm"]["controls"]
    ids = {item["id"] for item in owasp}
    assert "LLM01" in ids
    assert "LLM02" in ids


def test_cobertura_conta_fail_em_llm01() -> None:
    runner = TestRunner(settings=_settings())
    vuln = runner.run_campaign("vulnerable")
    doc = montar_relatorio(vuln, runner.summarize(vuln), _settings())
    cov = cobertura_por_framework(doc)
    llm01 = next(
        c for c in cov["frameworks"]["owasp_llm"]["controls"] if c["id"] == "LLM01"
    )
    assert llm01["fail"] >= 1
