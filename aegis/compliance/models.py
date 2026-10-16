"""Modelos de tags de conformidade por caso de teste."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

FRAMEWORK_KEYS = ("owasp_llm", "mitre_attack", "mitre_atlas", "nist_csf")


@dataclass(frozen=True)
class ComplianceTags:
    """Referências a controles/técnicas por framework."""

    owasp_llm: tuple[str, ...] = ()
    mitre_attack: tuple[str, ...] = ()
    mitre_atlas: tuple[str, ...] = ()
    nist_csf: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, list[str]]:
        return {
            "owasp_llm": list(self.owasp_llm),
            "mitre_attack": list(self.mitre_attack),
            "mitre_atlas": list(self.mitre_atlas),
            "nist_csf": list(self.nist_csf),
        }

    @classmethod
    def from_raw(cls, raw: dict[str, Any] | None) -> ComplianceTags:
        if not raw:
            return cls()
        return cls(
            owasp_llm=tuple(_lista(raw.get("owasp_llm"))),
            mitre_attack=tuple(_lista(raw.get("mitre_attack"))),
            mitre_atlas=tuple(_lista(raw.get("mitre_atlas"))),
            nist_csf=tuple(_lista(raw.get("nist_csf"))),
        )


def _lista(valor: Any) -> list[str]:
    if not valor:
        return []
    if isinstance(valor, str):
        return [valor]
    if isinstance(valor, list):
        return [str(v) for v in valor]
    return []
