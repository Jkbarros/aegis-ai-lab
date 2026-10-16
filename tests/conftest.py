"""
Fixtures compartilhadas do pytest (Etapa 5).

O `pythonpath = ["."]` em pyproject.toml permite `import aegis` sem hacks de sys.path.
"""

from __future__ import annotations

import pytest

from aegis.config import Settings
from aegis.evaluator import Evaluator
from aegis.models import Observation
from aegis.test_runner import TestRunner
from tests.constants import LAB_FAKE_SECRET


@pytest.fixture
def settings_teste() -> Settings:
    """Configuração isolada com segredo previsível para asserções."""
    return Settings(
        llm_provider="openai",
        openai_api_key=None,
        openai_model="gpt-4o-mini",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="llama3.2",
        llm_timeout_seconds=60.0,
        lab_fake_secret=LAB_FAKE_SECRET,
    )


@pytest.fixture
def settings_com_chave_openai(settings_teste: Settings) -> Settings:
    """Settings com chave fictícia (não chama a API)."""
    return Settings(
        llm_provider=settings_teste.llm_provider,
        openai_api_key="sk-test-fake-key-not-real",
        openai_model=settings_teste.openai_model,
        ollama_base_url=settings_teste.ollama_base_url,
        ollama_model=settings_teste.ollama_model,
        llm_timeout_seconds=settings_teste.llm_timeout_seconds,
        lab_fake_secret=settings_teste.lab_fake_secret,
    )


@pytest.fixture
def evaluator() -> Evaluator:
    return Evaluator()


@pytest.fixture
def runner(settings_teste: Settings) -> TestRunner:
    return TestRunner(settings=settings_teste)


@pytest.fixture
def observation_factory():
    """Cria Observation de teste com defaults."""

    def _make(
        response_text: str = "",
        user_input: str = "entrada de teste",
        profile: str = "test",
        error_message: str | None = None,
    ) -> Observation:
        return Observation(
            user_input=user_input,
            response_text=response_text,
            profile=profile,
            error_message=error_message,
        )

    return _make
