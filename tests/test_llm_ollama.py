"""Testes do cliente Ollama com mocks HTTP."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from aegis.config import Settings
from aegis.llm.base import ChatMessage, LLMError
from aegis.llm.ollama_client import OllamaChatClient


def _settings() -> Settings:
    return Settings(
        llm_provider="ollama",
        openai_api_key=None,
        openai_model="gpt-4o-mini",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="llama3.2",
        llm_timeout_seconds=5.0,
        lab_fake_secret="LAB-SECRET",
    )


@patch("aegis.llm.ollama_client.requests.post")
def test_chat_sucesso(mock_post: MagicMock) -> None:
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"message": {"role": "assistant", "content": "ok"}},
    )
    client = OllamaChatClient(_settings())
    assert client.chat([ChatMessage(role="user", content="oi")]) == "ok"


@patch("aegis.llm.ollama_client.requests.post")
def test_timeout(mock_post: MagicMock) -> None:
    mock_post.side_effect = requests.Timeout()
    client = OllamaChatClient(_settings())
    with pytest.raises(LLMError, match="Timeout"):
        client.chat([ChatMessage(role="user", content="oi")])


@patch("aegis.llm.ollama_client.requests.post")
def test_conexao_recusada(mock_post: MagicMock) -> None:
    mock_post.side_effect = requests.ConnectionError()
    client = OllamaChatClient(_settings())
    with pytest.raises(LLMError, match="conectar"):
        client.chat([ChatMessage(role="user", content="oi")])


@patch("aegis.llm.ollama_client.requests.post")
def test_http_erro(mock_post: MagicMock) -> None:
    mock_post.return_value = MagicMock(status_code=404, text="model not found")
    client = OllamaChatClient(_settings())
    with pytest.raises(LLMError, match="404"):
        client.chat([ChatMessage(role="user", content="oi")])
