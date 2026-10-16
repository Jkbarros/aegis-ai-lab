"""Testes do cliente OpenAI com mocks — falhas de comunicação sem API real."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from openai import APIConnectionError, APITimeoutError, RateLimitError

from aegis.config import Settings
from aegis.llm.base import ChatMessage, LLMError
from aegis.llm.openai_client import OpenAIChatClient


def _settings_com_chave() -> Settings:
    return Settings(
        llm_provider="openai",
        openai_api_key="sk-test-fake",
        openai_model="gpt-4o-mini",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="llama3.2",
        llm_timeout_seconds=1.0,
        lab_fake_secret="LAB-SECRET",
    )


def test_init_sem_chave_levanta_llm_error() -> None:
    cfg = _settings_com_chave()
    cfg_sem = Settings(
        llm_provider=cfg.llm_provider,
        openai_api_key=None,
        openai_model=cfg.openai_model,
        ollama_base_url=cfg.ollama_base_url,
        ollama_model=cfg.ollama_model,
        llm_timeout_seconds=cfg.llm_timeout_seconds,
        lab_fake_secret=cfg.lab_fake_secret,
    )
    with pytest.raises(LLMError, match="OPENAI_API_KEY"):
        OpenAIChatClient(cfg_sem)


def test_chat_lista_vazia() -> None:
    client = OpenAIChatClient(_settings_com_chave())
    with pytest.raises(LLMError, match="vazia"):
        client.chat([])


@patch("aegis.llm.openai_client.OpenAI")
def test_timeout_vira_llm_error(mock_openai_cls: MagicMock) -> None:
    instancia = mock_openai_cls.return_value
    instancia.chat.completions.create.side_effect = APITimeoutError(request=MagicMock())
    client = OpenAIChatClient(_settings_com_chave())
    with pytest.raises(LLMError, match="Timeout"):
        client.chat([ChatMessage(role="user", content="oi")])


@patch("aegis.llm.openai_client.OpenAI")
def test_conexao_vira_llm_error(mock_openai_cls: MagicMock) -> None:
    instancia = mock_openai_cls.return_value
    instancia.chat.completions.create.side_effect = APIConnectionError(request=MagicMock())
    client = OpenAIChatClient(_settings_com_chave())
    with pytest.raises(LLMError, match="conexão"):
        client.chat([ChatMessage(role="user", content="oi")])


@patch("aegis.llm.openai_client.OpenAI")
def test_rate_limit_vira_llm_error(mock_openai_cls: MagicMock) -> None:
    instancia = mock_openai_cls.return_value
    instancia.chat.completions.create.side_effect = RateLimitError(
        "rate limit",
        response=MagicMock(),
        body=None,
    )
    client = OpenAIChatClient(_settings_com_chave())
    with pytest.raises(LLMError, match="Limite de taxa"):
        client.chat([ChatMessage(role="user", content="oi")])


@patch("aegis.llm.openai_client.OpenAI")
def test_resposta_vazia_da_api(mock_openai_cls: MagicMock) -> None:
    instancia = mock_openai_cls.return_value
    instancia.chat.completions.create.return_value = MagicMock(choices=[])
    client = OpenAIChatClient(_settings_com_chave())
    with pytest.raises(LLMError, match="vazia ou inválida"):
        client.chat([ChatMessage(role="user", content="oi")])


@patch("aegis.llm.openai_client.OpenAI")
def test_chat_sucesso(mock_openai_cls: MagicMock) -> None:
    instancia = mock_openai_cls.return_value
    mensagem = MagicMock()
    mensagem.content = "resposta ok"
    instancia.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=mensagem)]
    )
    client = OpenAIChatClient(_settings_com_chave())
    assert client.chat([ChatMessage(role="user", content="oi")]) == "resposta ok"
