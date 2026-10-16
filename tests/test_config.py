"""Testes de configuração sem chave real de API."""

from __future__ import annotations

import pytest

from aegis.config import get_settings


@pytest.fixture
def sem_dotenv(monkeypatch: pytest.MonkeyPatch):
    """
    Impede que get_settings() leia o .env local durante o teste.

    Sem isso, load_dotenv repõe OPENAI_API_KEY depois do monkeypatch.delenv.
    """
    monkeypatch.setattr("aegis.config._carregar_dotenv", lambda: None)


def test_settings_openai_sem_chave(monkeypatch: pytest.MonkeyPatch, sem_dotenv: None) -> None:
    """Provedor openai com chave ausente (ambiente de teste isolado)."""
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    cfg = get_settings()
    assert cfg.llm_provider == "openai"
    assert cfg.openai_api_key is None or cfg.openai_api_key == ""


def test_settings_ollama_do_ambiente(monkeypatch: pytest.MonkeyPatch, sem_dotenv: None) -> None:
    """Provedor ollama definido só pelo ambiente do teste."""
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.2")
    cfg = get_settings()
    assert cfg.llm_provider == "ollama"
    assert cfg.ollama_model == "llama3.2"
