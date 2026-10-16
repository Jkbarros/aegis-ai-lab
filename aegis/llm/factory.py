"""Cria o cliente de LLM conforme LLM_PROVIDER no ambiente."""

from __future__ import annotations

from aegis.config import Settings, get_settings
from aegis.llm.base import LLMClient, LLMError
from aegis.llm.ollama_client import OllamaChatClient
from aegis.llm.openai_client import OpenAIChatClient


def create_llm_client(settings: Settings | None = None) -> LLMClient:
    """Instancia o provedor configurado (`openai` ou `ollama`)."""
    cfg = settings or get_settings()

    if cfg.llm_provider == "openai":
        return OpenAIChatClient(cfg)

    if cfg.llm_provider == "ollama":
        return OllamaChatClient(cfg)

    raise LLMError(
        f"Provedor LLM não suportado: '{cfg.llm_provider}'. "
        "Use LLM_PROVIDER=openai ou LLM_PROVIDER=ollama no .env."
    )
