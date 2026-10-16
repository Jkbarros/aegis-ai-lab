"""
Etapa 11 — demonstração de portfólio (~5 min com docs/DEMO.md).

  python scripts/demo_etapa11.py
  python scripts/demo_etapa11.py --full
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.config import Settings
from aegis.metrics import calcular_metricas
from aegis.reporter import executar_e_salvar_campanha
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


def _pause(msg: str, seconds: float = 0.0) -> None:
    print(msg)
    if seconds > 0:
        time.sleep(seconds)


def _run_pytest_quick() -> int:
    return subprocess.call(
        [sys.executable, "-m", "pytest", "-q", "--tb=no"],
        cwd=RAIZ,
    )


def _run_security_check() -> int:
    script = RAIZ / "scripts" / "check_security_lab.py"
    return subprocess.call([sys.executable, str(script)], cwd=RAIZ)


def _campanhas_demo(runner: TestRunner) -> None:
    _pause("\n[2/3] Campanhas simuladas (vulnerable vs hardened)...")
    rel_v, path_v = executar_e_salvar_campanha("vulnerable", runner)
    rel_h, path_h = executar_e_salvar_campanha("hardened", runner)
    m_v = calcular_metricas(rel_v)
    m_h = calcular_metricas(rel_h)
    print(f"  vulnerable -> FAIL rate {m_v.fail_rate:.1%} ({m_v.failed}/{m_v.total})  [{path_v.name}]")
    print(f"  hardened   -> FAIL rate {m_h.fail_rate:.1%} ({m_h.failed}/{m_h.total})  [{path_h.name}]")
    if rel_v.get("security", {}).get("sanitized_for_export"):
        print("  Relatórios sanitizados para export (Etapa 10).")


def main() -> int:
    parser = argparse.ArgumentParser(description="Demo portfólio — Aegis AI Lab")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Inclui pytest e checklist de segurança antes das campanhas",
    )
    parser.add_argument(
        "--skip-campaigns",
        action="store_true",
        help="Só imprime roteiro (útil em CI rápido)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Aegis AI Lab — demonstração (Etapa 11)")
    print("Roteiro completo: docs/DEMO.md")
    print("=" * 60)

    if args.full:
        _pause("\n[1/3] Testes automatizados (pytest)...")
        if _run_pytest_quick() != 0:
            print("pytest falhou — corrija antes da demo pública.")
            return 1
        _pause("\n[1/3] Checklist de segurança...")
        if _run_security_check() != 0:
            return 1
    else:
        _pause("\nDica: use --full para rodar pytest + check_security_lab antes.")

    if not args.skip_campaigns:
        runner = TestRunner(settings=_settings())
        _campanhas_demo(runner)

    _pause("\n[3/3] Próximo passo manual (gravação de tela):")
    print("  streamlit run app.py")
    print("  Executar Testes -> Resultados -> Relatorios")
    print("\nArquitetura: docs/ARCHITECTURE.md")
    print("Screenshots: docs/screenshots/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
