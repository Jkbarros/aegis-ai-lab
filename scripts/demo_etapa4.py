"""
Demonstração da Etapa 4 — biblioteca JSON + executor de campanha.

Execute:
  python scripts/demo_etapa4.py
  python scripts/demo_etapa4.py --profile protected
  python scripts/demo_etapa4.py --category prompt_injection
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.case_loader import load_all_cases
from aegis.test_runner import TestRunner


def main() -> int:
    parser = argparse.ArgumentParser(description="Executa campanha da biblioteca JSON")
    parser.add_argument(
        "--profile",
        choices=("vulnerable", "protected"),
        action="append",
        help="Perfil da app (pode repetir; padrão: ambos)",
    )
    parser.add_argument(
        "--category",
        action="append",
        help="Filtrar por risk_category (ex.: prompt_injection)",
    )
    args = parser.parse_args()

    perfis = args.profile or ["vulnerable", "protected"]
    categorias = set(args.category) if args.category else None

    runner = TestRunner()
    casos = load_all_cases()
    print("=" * 70)
    print("Aegis AI Lab — Etapa 4: biblioteca de casos + runner")
    print("=" * 70)
    print(f"Casos carregados: {len(casos)}")
    if categorias:
        print(f"Filtro de categoria: {', '.join(sorted(categorias))}")
    print()

    falhas_expectativa = 0

    for perfil in perfis:
        resultados = runner.run_campaign(perfil, categories=categorias)
        resumo = runner.summarize(resultados)

        print(f"--- Perfil: {perfil} ---")
        print(
            f"Total: {resumo.total} | PASS: {resumo.passed} | FAIL: {resumo.failed} | "
            f"ERROR: {resumo.errors} | INCONCLUSIVE: {resumo.inconclusive} | "
            f"Expectativa divergente: {resumo.expectation_mismatches}"
        )

        for item in resultados:
            exp = item.expected_verdict.value if item.expected_verdict else "-"
            ok = "ok" if item.expectation_met is not False else "DIVERGE"
            if item.expectation_met is False:
                falhas_expectativa += 1
            print(
                f"  [{item.verdict.status.value:12}] [{ok:7}] {item.case.id} "
                f"(esperado {exp}) {item.case.name}"
            )
        print()

    if falhas_expectativa:
        print(f"Atenção: {falhas_expectativa} caso(s) não bateram com expectations do JSON.")
        return 1

    print("Todos os casos alinharam com as expectations definidas na biblioteca JSON.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
