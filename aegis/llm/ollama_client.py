"""
Cliente Ollama via API HTTP local (sem SDK extra — usa requests).

Documentação: https://github.com/ollama/ollama/blob/main/docs/api.md
"""

from __future__ import annotations

import requests

from aegis.config import Settings
from aegis.llm.base import ChatMessage, LLMError


class OllamaChatClient:
    """Envia mensagens para POST /api/chat no serviço Ollama local."""

    def __init__(self, settings: Settings) -> None:
        base = settings.ollama_base_url.rstrip("/")
        self._chat_url = f"{base}/api/chat"
        self._model = settings.ollama_model
        self._timeout = settings.llm_timeout_seconds

    @property
    def provider_name(self) -> str:
        return "ollama"

    @property
    def model_name(self) -> str:
        return self._model

    def chat(self, messages: list[ChatMessage]) -> str:
        if not messages:
            raise LLMError("Lista de mensagens vazia.")

        payload = {
            "model": self._model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
        }

        try:
            resposta = requests.post(self._chat_url, json=payload, timeout=self._timeout)
        except requests.Timeout as exc:
            raise LLMError(f"Timeout ao chamar Ollama ({self._model}).") from exc
        except requests.ConnectionError as exc:
            raise LLMError(
                "Não foi possível conectar ao Ollama. Verifique se o app está aberto em "
                "http://127.0.0.1:11434"
            ) from exc
        except requests.RequestException as exc:
            raise LLMError(f"Erro HTTP ao chamar Ollama: {exc}") from exc

        if resposta.status_code != 200:
            raise LLMError(
                f"Ollama retornou HTTP {resposta.status_code}: {resposta.text[:300]}"
            )

        try:
            dados = resposta.json()
        except ValueError as exc:
            raise LLMError("Resposta JSON inválida do Ollama.") from exc

        mensagem = dados.get("message") or {}
        conteudo = mensagem.get("content")
        if not conteudo:
            raise LLMError("Resposta vazia ou inválida do Ollama.")

        return str(conteudo)
