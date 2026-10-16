"""Testes de configuração sem chave real de API."""

from __future__ import annotations

import pytest

from aegis.config import get_settings


def test_settings_openai_sem_chave(monkeypatch: pytest.MonkeyPatch) -> None:
    """Isolado do .env local: provedor openai e chave ausente."""
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    cfg = get_settings()
    assert cfg.llm_provider == "openai"
    assert cfg.openai_api_key is None or cfg.openai_api_key == ""


def test_settings_ollama_do_ambiente(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reflete o uso local com Ollama (como no .env.example atual)."""
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.2")
    cfg = get_settings()
    assert cfg.llm_provider == "ollama"
    assert cfg.ollama_model == "llama3.2"
