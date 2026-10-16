"""Cria o cliente de LLM conforme LLM_PROVIDER no ambiente."""

from __future__ import annotations

from aegis.config import Settings, get_settings
from aegis.llm.base import LLMClient, LLMError
from aegis.llm.openai_client import OpenAIChatClient


def create_llm_client(settings: Settings | None = None) -> LLMClient:
    """
    Instancia o provedor configurado.

    Hoje: apenas `openai`. Na Etapa 6 adicionaremos `ollama`.
    """
    cfg = settings or get_settings()

    if cfg.llm_provider == "openai":
        return OpenAIChatClient(cfg)

    raise LLMError(
        f"Provedor LLM não suportado: '{cfg.llm_provider}'. "
        "Use LLM_PROVIDER=openai no .env (Ollama virá na Etapa 6)."
    )
