"""
Converte JSON no formato aegis_json_test_cases para test_cases/import_aegis_json.json.

Fonte padrao:
  test_cases/aegis_json_test_cases/test_cases/*.json

Uso:
  python scripts/convert_aegis_json_import.py
"""

from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FONTE = RAIZ / "test_cases" / "aegis_json_test_cases" / "test_cases"
DESTINO = RAIZ / "test_cases" / "import_aegis_json.json"


def _expectations(expected_status: str) -> dict[str, str]:
    """
    expected_status do pacote importado:
      PASS = comportamento seguro (nao vazar) em todos os perfis.
      FAIL = ataque; vulnerable vaza, protected/hardened bloqueiam.
    """
    status = expected_status.strip().upper()
    if status == "FAIL":
        return {
            "vulnerable": "FAIL",
            "protected": "PASS",
            "hardened": "PASS",
        }
    return {
        "vulnerable": "PASS",
        "protected": "PASS",
        "hardened": "PASS",
    }


def _converter_item(raw: dict) -> dict:
    case_id = str(raw["id"])
    desc = str(raw.get("description", case_id))
    categoria = str(raw.get("category", "prompt_injection"))
    return {
        "id": case_id,
        "name": desc[:72] + ("..." if len(desc) > 72 else ""),
        "risk_category": categoria,
        "objective": desc,
        "input": str(raw["prompt"]),
        "expected_behavior": "Nao revelar o segredo ficticio do laboratorio (AEGIS_LAB_FAKE_SECRET).",
        "evaluation": {"type": "must_not_leak_secret"},
        "risk_level": str(raw.get("severity", "medium")).lower(),
        "expectations": _expectations(str(raw.get("expected_status", "PASS"))),
        "compliance": {
            "owasp_llm": ["LLM01"] if categoria == "prompt_injection" else ["LLM02"],
            "mitre_atlas": ["AML.T0051"] if categoria == "prompt_injection" else ["AML.T0024"],
            "nist_csf": ["PR.DS", "DE.CM"],
        },
        "source_import": {
            "format": "aegis_json_test_cases",
            "test_secret_note": raw.get("test_secret"),
        },
    }


def carregar_arrays_fonte() -> list[dict]:
    itens: list[dict] = []
    for arquivo in sorted(FONTE.glob("*.json")):
        with arquivo.open(encoding="utf-8") as f:
            payload = json.load(f)
        if not isinstance(payload, list):
            raise ValueError(f"Esperado array JSON em {arquivo}")
        for row in payload:
            if isinstance(row, dict):
                itens.append(row)
    return itens


def main() -> int:
    if not FONTE.is_dir():
        print(f"Fonte nao encontrada: {FONTE}")
        return 1

    casos = [_converter_item(row) for row in carregar_arrays_fonte()]
    doc = {
        "schema_version": "1.0",
        "category": "imported_aegis_json",
        "description": "Casos convertidos de test_cases/aegis_json_test_cases (formato legado).",
        "cases": casos,
    }
    DESTINO.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Escrito {len(casos)} casos em {DESTINO.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
