"""
Cliente OpenAI usando o SDK oficial.

Requisitos:
- Variável OPENAI_API_KEY no ambiente ou no arquivo `.env` local.
"""

from __future__ import annotations

from openai import APIConnectionError, APITimeoutError, OpenAI, RateLimitError

from aegis.config import Settings
from aegis.llm.base import ChatMessage, LLMError


class OpenAIChatClient:
    """Implementação de LLMClient para a API de chat da OpenAI."""

    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise LLMError(
                "OPENAI_API_KEY não configurada. Copie .env.example para .env e defina a chave."
            )

        self._model = settings.openai_model
        self._client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.llm_timeout_seconds,
        )

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model_name(self) -> str:
        return self._model

    def chat(self, messages: list[ChatMessage]) -> str:
        if not messages:
            raise LLMError("Lista de mensagens vazia.")

        payload = [{"role": m.role, "content": m.content} for m in messages]

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=payload,
            )
        except APITimeoutError as exc:
            raise LLMError(f"Timeout ao chamar OpenAI ({self._model}).") from exc
        except APIConnectionError as exc:
            raise LLMError("Falha de conexão com a API OpenAI.") from exc
        except RateLimitError as exc:
            raise LLMError("Limite de taxa da OpenAI atingido. Tente novamente mais tarde.") from exc
        except Exception as exc:  # noqa: BLE001 — encapsulamos para o laboratório
            raise LLMError(f"Erro inesperado na OpenAI: {exc}") from exc

        choice = response.choices[0] if response.choices else None
        if choice is None or choice.message.content is None:
            raise LLMError("Resposta vazia ou inválida da OpenAI.")

        return choice.message.content
