"""Testes de configuração sem chave real de API."""

from __future__ import annotations

import pytest

from aegis.config import get_settings


def test_settings_sem_chave(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    cfg = get_settings()
    assert cfg.llm_provider == "openai"
    assert cfg.openai_api_key is None or isinstance(cfg.openai_api_key, str)
