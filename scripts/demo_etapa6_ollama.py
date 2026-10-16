"""
Etapa 6 — executa um caso da biblioteca contra Llama 3.2 via Ollama.

Requer: Ollama rodando, modelo llama3.2 instalado, .env com LLM_PROVIDER=ollama

  python scripts/demo_etapa6_ollama.py
  python scripts/demo_etapa6_ollama.py --case pi-001
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
from aegis.target.llm_assistant import LLMLabAssistant


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", default="pi-001", help="ID do caso em test_cases/*.json")
    parser.add_argument(
        "--profile",
        default="protected",
        choices=("protected", "vulnerable"),
        help="Prompt system do assistente LLM",
    )
    args = parser.parse_args()

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

    caso = next((c for c in load_all_cases() if c.id == args.case), None)
    if caso is None:
        print(f"Caso não encontrado: {args.case}")
        return 1

    print("=" * 70)
    print("Aegis AI Lab — Etapa 6: caso real com Ollama")
    print("=" * 70)
    print(f"Modelo: {settings.ollama_model} @ {settings.ollama_base_url}")
    print(f"Caso:   {caso.id} — {caso.name}")
    print(f"Perfil: llm_{args.profile}")
    print()

    app = LLMLabAssistant(args.profile, settings)
    saida = app.respond(caso.user_input)

    print("Entrada:")
    print(caso.user_input)
    print()
    print("Resposta do modelo:")
    print(saida.text)
    print()

    veredito = Evaluator().evaluate(
        Observation(user_input=caso.user_input, response_text=saida.text, profile=saida.profile),
        caso.evaluation,
        lab_secret=settings.lab_fake_secret,
    )

    print(f"Veredito: {veredito.status.value}")
    print(veredito.summary)
    for ev in veredito.evidence:
        print(f"  - {ev.code}: {ev.message}")

    print()
    print("Nota: LLMs podem variar; use o veredito + evidências, não só impressão subjetiva.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
