"""
Demonstração da Etapa 3 — avaliador com PASS / FAIL / ERROR / INCONCLUSIVE.

Execute:
  python scripts/demo_etapa3.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.config import get_settings
from aegis.evaluator import Evaluator
from aegis.lab import CASOS_DEMO_ETAPA2, criar_assistente
from aegis.models import CriterionType, EvaluationCriterion, Observation


def main() -> int:
    cfg = get_settings()
    avaliador = Evaluator()
    criterio = EvaluationCriterion(type=CriterionType.MUST_NOT_LEAK_SECRET)

    print("=" * 70)
    print("Aegis AI Lab — Etapa 3: motor de avaliação")
    print("=" * 70)
    print(f"Critério: {criterio.type.value}")
    print()

    for perfil in ("vulnerable", "protected"):
        app = criar_assistente(perfil, cfg)
        print(f"--- Perfil: {perfil} ---")
        for entrada in CASOS_DEMO_ETAPA2:
            saida = app.respond(entrada)
            veredito = avaliador.evaluate(
                Observation(user_input=entrada, response_text=saida.text, profile=perfil),
                criterio,
                lab_secret=cfg.lab_fake_secret,
            )
            print(f"[{veredito.status.value:12}] {entrada[:55]}{'...' if len(entrada) > 55 else ''}")
            print(f"             {veredito.summary}")
            for ev in veredito.evidence:
                linha = f"             · {ev.code}: {ev.message}"
                if ev.snippet:
                    linha += f" | trecho: {ev.snippet!r}"
                print(linha)
        print()

    print("Interpretação didática:")
    print("- vulnerable + ataques: esperado FAIL (vazamento).")
    print("- protected + mesmos ataques: esperado PASS.")
    print("- INCONCLUSIVE aparece em casos ambíguos (ver tests/test_evaluator.py).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
