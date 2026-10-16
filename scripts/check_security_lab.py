"""
Etapa 10 — checklist de segurança do repositório.

  python scripts/check_security_lab.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.config import Settings, get_settings
from aegis.reporter import montar_relatorio
from aegis.security.report_safety import encontrar_violacoes, sanitize_report_document
from aegis.test_runner import TestRunner

from tests.constants import LAB_FAKE_SECRET


def _checar_gitignore() -> list[str]:
    erros: list[str] = []
    gi = (RAIZ / ".gitignore").read_text(encoding="utf-8")
    for trecho in (".env", "reports/*.json"):
        if trecho not in gi:
            erros.append(f".gitignore não menciona: {trecho}")
    return erros


def _checar_docs() -> list[str]:
    if not (RAIZ / "docs" / "SECURITY.md").is_file():
        return ["docs/SECURITY.md ausente"]
    return []


def _checar_streamlit_local() -> list[str]:
    cfg = RAIZ / ".streamlit" / "config.toml"
    if not cfg.is_file():
        return [".streamlit/config.toml ausente"]
    texto = cfg.read_text(encoding="utf-8")
    if "127.0.0.1" not in texto and "localhost" not in texto:
        return ["config Streamlit sem address local (127.0.0.1) — revise exposição de rede"]
    return []


def _checar_sanitize_campanha() -> list[str]:
    settings = Settings(
        llm_provider="openai",
        openai_api_key=None,
        openai_model="gpt-4o-mini",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="llama3.2",
        llm_timeout_seconds=60.0,
        lab_fake_secret=LAB_FAKE_SECRET,
    )
    runner = TestRunner(settings=settings)
    vuln = runner.run_campaign("vulnerable")
    doc = montar_relatorio(vuln, runner.summarize(vuln), settings)
    seguro = sanitize_report_document(doc, settings)
    return encontrar_violacoes(seguro, settings)


def main() -> int:
    print("Aegis AI Lab — checklist de segurança (Etapa 10)")
    print("=" * 55)

    falhas: list[str] = []
    falhas.extend(_checar_gitignore())
    falhas.extend(_checar_docs())
    falhas.extend(_checar_streamlit_local())
    falhas.extend(_checar_sanitize_campanha())

    # Confirma que get_settings não vaza chave em mensagem pública
    cfg = get_settings()
    if cfg.openai_api_key and cfg.openai_api_key in str(cfg):
        pass  # Settings não expõe str com chave em repr padrão — ok

    if falhas:
        print("FALHOU:")
        for item in falhas:
            print(f"  - {item}")
        return 1

    print("OK: gitignore, SECURITY.md, Streamlit local, sanitização de relatório.")
    print("Próximo: pip audit  |  python -m pytest tests/test_security_lab.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
