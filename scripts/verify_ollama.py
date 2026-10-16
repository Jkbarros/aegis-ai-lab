"""
Verifica Ollama + modelo configurado.

  python scripts/verify_ollama.py
  python scripts/verify_ollama.py --ping
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.config import get_settings
from aegis.llm.base import ChatMessage, LLMError
from aegis.llm.factory import create_llm_client


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica Ollama no Aegis AI Lab")
    parser.add_argument("--ping", action="store_true", help="Envia uma mensagem de teste ao modelo")
    args = parser.parse_args()

    settings = get_settings()
    print(f"Provedor (env): {settings.llm_provider}")
    print(f"Ollama URL:     {settings.ollama_base_url}")
    print(f"Modelo:         {settings.ollama_model}")
    print()
    print("Para usar Ollama neste projeto, defina no .env:")
    print("  LLM_PROVIDER=ollama")
    print("  OLLAMA_MODEL=llama3.2")

    if not args.ping:
        print()
        print("Use --ping para testar uma geração real (pode demorar na primeira vez).")
        return 0

    cfg = settings
    if settings.llm_provider != "ollama":
        from aegis.config import Settings

        cfg = Settings(
            llm_provider="ollama",
            openai_api_key=settings.openai_api_key,
            openai_model=settings.openai_model,
            ollama_base_url=settings.ollama_base_url,
            ollama_model=settings.ollama_model,
            llm_timeout_seconds=settings.llm_timeout_seconds,
            lab_fake_secret=settings.lab_fake_secret,
        )

    try:
        client = create_llm_client(cfg)
        texto = client.chat(
            [
                ChatMessage(role="system", content="Responda em uma frase curta."),
                ChatMessage(role="user", content="Diga apenas: conexao OK."),
            ]
        )
    except LLMError as exc:
        print(f"ERRO: {exc}")
        return 1

    print("Resposta do modelo:")
    print(texto.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
