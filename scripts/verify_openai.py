"""
Verifica se a OpenAI está configurada (opcional: uma chamada mínima).

Uso (na raiz do projeto, com .venv ativo):
  python scripts/verify_openai.py
  python scripts/verify_openai.py --ping

--ping envia uma pergunta curta e gasta créditos da sua conta OpenAI.
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
    parser = argparse.ArgumentParser(description="Verifica configuração OpenAI do Aegis AI Lab")
    parser.add_argument(
        "--ping",
        action="store_true",
        help="Envia uma mensagem de teste real à API (usa créditos)",
    )
    args = parser.parse_args()

    settings = get_settings()
    print(f"Provedor: {settings.llm_provider}")
    print(f"Modelo:   {settings.openai_model}")

    if not settings.openai_api_key:
        print("ERRO: OPENAI_API_KEY ausente. Copie .env.example para .env e preencha a chave.")
        return 1

    print("OK: OPENAI_API_KEY presente (valor não exibido por segurança).")

    if not args.ping:
        print("Dica: use --ping para testar uma chamada real à API.")
        return 0

    try:
        client = create_llm_client(settings)
        resposta = client.chat(
            [
                ChatMessage(role="system", content="Responda em uma frase curta."),
                ChatMessage(role="user", content="Diga apenas: conexão OK."),
            ]
        )
    except LLMError as exc:
        print(f"ERRO na chamada: {exc}")
        return 1

    print("Resposta do modelo:")
    print(resposta.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
