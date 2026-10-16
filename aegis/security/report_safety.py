"""
Sanitização de relatórios e auditoria (Etapa 10).

Relatórios em reports/ podem ser compartilhados; não devem conter chaves reais
nem o valor bruto de segredos configurados no .env.
"""

from __future__ import annotations

import copy
import json
import re
from typing import Any

from aegis.config import Settings

_REDACT_LAB = "[REDACTED_LAB_SECRET]"
_REDACT_API_KEY = "[REDACTED_API_KEY]"
_OPENAI_KEY_RE = re.compile(r"\bsk-[a-zA-Z0-9_-]{20,}\b")
_FORBIDDEN_TOP_LEVEL_KEYS = frozenset(
    {"openai_api_key", "OPENAI_API_KEY", "api_key", "password", "token"}
)


def redact_string(text: str, settings: Settings) -> str:
    if not text:
        return text
    out = text
    segredo = settings.lab_fake_secret
    if segredo and len(segredo) >= 6:
        out = out.replace(segredo, _REDACT_LAB)
    out = _OPENAI_KEY_RE.sub(_REDACT_API_KEY, out)
    if settings.openai_api_key and len(settings.openai_api_key) >= 8:
        out = out.replace(settings.openai_api_key, _REDACT_API_KEY)
    return out


def _walk_sanitize(obj: Any, settings: Settings) -> Any:
    if isinstance(obj, str):
        return redact_string(obj, settings)
    if isinstance(obj, list):
        return [_walk_sanitize(item, settings) for item in obj]
    if isinstance(obj, dict):
        return {k: _walk_sanitize(v, settings) for k, v in obj.items()}
    return obj


def sanitize_report_document(relatorio: dict[str, Any], settings: Settings) -> dict[str, Any]:
    """Cópia do relatório com strings sensíveis mascaradas."""
    doc = _walk_sanitize(copy.deepcopy(relatorio), settings)
    doc["security"] = {
        "sanitized_for_export": True,
        "api_keys_included": False,
        "lab_secret_redaction": _REDACT_LAB,
        "note": (
            "Respostas simuladas podem indicar vazamento (FAIL) sem repetir o segredo real do .env."
        ),
    }
    return doc


def encontrar_violacoes(relatorio: dict[str, Any], settings: Settings) -> list[str]:
    """Lista problemas se o documento ainda contiver material que não deveria ser exportado."""
    violacoes: list[str] = []

    for chave in _FORBIDDEN_TOP_LEVEL_KEYS:
        if chave in relatorio:
            violacoes.append(f"chave proibida no relatório: {chave}")

    payload = json.dumps(relatorio, ensure_ascii=False)
    if settings.openai_api_key and settings.openai_api_key in payload:
        violacoes.append("OPENAI_API_KEY aparece no JSON do relatório")
    if _OPENAI_KEY_RE.search(payload):
        violacoes.append("padrão de chave OpenAI (sk-...) detectado no relatório")
    segredo = settings.lab_fake_secret
    if segredo and len(segredo) >= 6 and segredo in payload:
        violacoes.append("valor de AEGIS_LAB_FAKE_SECRET aparece sem redação no relatório")

    lab = relatorio.get("lab") or {}
    if isinstance(lab, dict) and "openai_api_key" in lab:
        violacoes.append("campo lab.openai_api_key não deve existir")

    return violacoes


def relatorio_seguro_para_export(relatorio: dict[str, Any], settings: Settings) -> bool:
    return not encontrar_violacoes(sanitize_report_document(relatorio, settings), settings)
