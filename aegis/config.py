"""
Configuração central do Aegis AI Lab.

Lê variáveis de ambiente (e opcionalmente o arquivo `.env` local via python-dotenv).
Nunca coloque chaves reais no código — apenas em `.env` na sua máquina.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _carregar_dotenv() -> None:
    """Carrega `.env` na raiz do projeto, se existir e se dotenv estiver instalado."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    raiz = Path(__file__).resolve().parents[1]
    env_path = raiz / ".env"
    if env_path.is_file():
        load_dotenv(env_path)


@dataclass(frozen=True)
class Settings:
    """Valores de configuração usados pelo laboratório."""

    llm_provider: str
    openai_api_key: str | None
    openai_model: str
    llm_timeout_seconds: float
    lab_fake_secret: str


def get_settings() -> Settings:
    """
    Monta a configuração a partir do ambiente.

    Retorno:
        Settings com valores atuais (chave OpenAI pode ser None se não configurada).
    """
    _carregar_dotenv()

    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    timeout_raw = os.getenv("LLM_TIMEOUT_SECONDS", "60").strip()

    try:
        timeout = float(timeout_raw)
    except ValueError:
        timeout = 60.0

    return Settings(
        llm_provider=provider,
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip(),
        llm_timeout_seconds=timeout,
        lab_fake_secret=os.getenv(
            "AEGIS_LAB_FAKE_SECRET",
            "LAB-ONLY-DO-NOT-USE-IN-PRODUCTION",
        ).strip(),
    )
