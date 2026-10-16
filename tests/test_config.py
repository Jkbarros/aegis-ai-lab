"""Testes de configuração sem chave real de API."""

from __future__ import annotations

import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))


def test_settings_sem_chave() -> None:
    os.environ.pop("OPENAI_API_KEY", None)
    from aegis.config import get_settings

    cfg = get_settings()
    assert cfg.llm_provider == "openai"
    assert cfg.openai_api_key is None or isinstance(cfg.openai_api_key, str)


if __name__ == "__main__":
    test_settings_sem_chave()
    print("OK: tests/test_config.py passou.")
