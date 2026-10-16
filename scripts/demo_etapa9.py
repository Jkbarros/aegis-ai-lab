"""
Etapa 9 — demonstra métricas e comparação entre campanhas salvas.

Execute após ter pelo menos duas campanhas em reports/ (ex.: vulnerable e hardened):
  python scripts/demo_etapa9.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.config import Settings
from aegis.metrics import calcular_metricas
from aegis.reporter import (
    comparar_campanhas_salvas,
    executar_e_salvar_campanha,
    listar_relatorios,
)
from aegis.test_runner import TestRunner

_LAB_FAKE_SECRET = "LAB-FAKE-SECRET-FOR-DEMO"


def _settings() -> Settings:
    return Settings(
        llm_provider="openai",
        openai_api_key=None,
        openai_model="gpt-4o-mini",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="llama3.2",
        llm_timeout_seconds=60.0,
        lab_fake_secret=_LAB_FAKE_SECRET,
    )


def main() -> int:
    runner = TestRunner(settings=_settings())
    if len(listar_relatorios()) < 2:
        print("Gerando campanhas de exemplo (vulnerable e hardened)...")
        executar_e_salvar_campanha("vulnerable", runner)
        executar_e_salvar_campanha("hardened", runner)

    arquivos = listar_relatorios()
    vuln = next((p for p in arquivos if "_vulnerable" in p.name), arquivos[-1])
    hard = next((p for p in arquivos if "_hardened" in p.name), arquivos[0])

    from aegis.reporter import carregar_relatorio

    m_v = calcular_metricas(carregar_relatorio(vuln))
    m_h = calcular_metricas(carregar_relatorio(hard))
    print(f"vulnerable: FAIL rate {m_v.fail_rate:.1%} ({m_v.failed}/{m_v.total})")
    print(f"hardened:   FAIL rate {m_h.fail_rate:.1%} ({m_h.failed}/{m_h.total})")

    diff = comparar_campanhas_salvas(vuln, hard)
    print(f"Melhorias FAIL->PASS: {diff['improved_fail_to_pass']}")
    print(f"Delta taxa FAIL: {diff['fail_rate_delta']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
