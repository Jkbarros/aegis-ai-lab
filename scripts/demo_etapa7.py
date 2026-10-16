"""
Etapa 7 — compara perfis vulnerable / protected / hardened (app simulada).

Opcional: um caso com LLM hardened (Ollama), mais lento e não determinístico.

  python scripts/demo_etapa7.py
  python scripts/demo_etapa7.py --llm --case pi-002
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.case_loader import load_all_cases
from aegis.config import Settings, get_settings
from aegis.evaluator import Evaluator
from aegis.models import Observation
from aegis.test_runner import TestRunner
from aegis.target.llm_hardened import LLMHardenedAssistant


def main() -> int:
    parser = argparse.ArgumentParser(description="Demo Etapa 7 — controles de segurança")
    parser.add_argument("--llm", action="store_true", help="Inclui um caso com Ollama (llm_hardened)")
    parser.add_argument("--case", default="pi-002", help="Caso para teste LLM")
    args = parser.parse_args()

    runner = TestRunner()
    perfis = ("vulnerable", "protected", "hardened")
    ev = Evaluator()

    print("=" * 70)
    print("Aegis AI Lab — Etapa 7: controles hardened (simulado)")
    print("=" * 70)
    print("Controles: validacao de entrada, envelope nao confiavel (LLM), filtro de saida.")
    print("Limitacao: heuristica nao cobre todos os ataques; LLM pode variar.")
    print()

    divergencias_total = 0
    for perfil in perfis:
        resultados = runner.run_campaign(perfil)
        resumo = runner.summarize(resultados)
        divergencias_total += resumo.expectation_mismatches
        print(
            f"[{perfil:10}] total={resumo.total} PASS={resumo.passed} FAIL={resumo.failed} "
            f"divergencias_expectativa={resumo.expectation_mismatches}"
        )

    print()
    print("Detalhe pi-002 (injection direta):")
    caso = next(c for c in load_all_cases() if c.id == "pi-002")
    for perfil in perfis:
        r = runner.run_case(caso, perfil)
        trecho = r.observation.response_text.replace("\n", " ")[:100]
        print(f"  {perfil:10} -> {r.verdict.status.value} | {trecho}")

    if divergencias_total:
        print(f"\nAtencao: {divergencias_total} divergencia(s) vs expectations JSON.")
        return 1

    print("\nSimulado: expectations JSON alinhadas para vulnerable/protected/hardened.")

    if args.llm:
        print()
        print("--- LLM hardened (Ollama) ---")
        base = get_settings()
        settings = Settings(
            llm_provider="ollama",
            openai_api_key=base.openai_api_key,
            openai_model=base.openai_model,
            ollama_base_url=base.ollama_base_url,
            ollama_model=base.ollama_model,
            llm_timeout_seconds=max(base.llm_timeout_seconds, 120.0),
            lab_fake_secret=base.lab_fake_secret,
        )
        caso_llm = next((c for c in load_all_cases() if c.id == args.case), None)
        if not caso_llm:
            print(f"Caso {args.case} nao encontrado.")
            return 1
        app = LLMHardenedAssistant(settings)
        saida = app.respond(caso_llm.user_input)
        veredito = ev.evaluate(
            Observation(
                user_input=caso_llm.user_input,
                response_text=saida.text,
                profile=saida.profile,
            ),
            caso_llm.evaluation,
            lab_secret=settings.lab_fake_secret,
        )
        print(f"Caso {args.case} | Veredito: {veredito.status.value}")
        print(saida.text[:500])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
