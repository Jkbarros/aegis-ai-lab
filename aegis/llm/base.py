"""
Contrato comum para provedores de LLM.

Usar uma interface pequena facilita trocar OpenAI por Ollama sem reescrever o laboratório.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class LLMError(Exception):
    """Erro ao comunicar com o provedor de modelo (rede, API, timeout, etc.)."""


@dataclass(frozen=True)
class ChatMessage:
    """Uma mensagem no formato papel + conteúdo."""

    role: str
    content: str


class LLMClient(Protocol):
    """Interface mínima que o motor de testes usará nas etapas seguintes."""

    @property
    def provider_name(self) -> str:
        """Nome do provedor (ex.: openai, ollama)."""

    @property
    def model_name(self) -> str:
        """Identificador do modelo em uso."""

    def chat(self, messages: list[ChatMessage]) -> str:
        """
        Envia mensagens e devolve o texto da resposta do assistente.

        Raises:
            LLMError: falha de comunicação ou resposta inválida.
        """
