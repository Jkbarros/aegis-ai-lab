"""Smoke test da preparacao de demo para README."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAMPLES = RAIZ / "docs" / "samples"


def test_samples_manifesto_existe() -> None:
    manifest = SAMPLES / "manifest.json"
    assert manifest.is_file()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert "hardened" in data.get("profiles", [])


def test_sample_hardened_sem_segredo_bruto() -> None:
    path = SAMPLES / "campaign_demo_hardened.json"
    assert path.is_file()
    texto = path.read_text(encoding="utf-8")
    assert "LAB-DEMO-CONTROLLED-ENV-ONLY" not in texto
    assert "[REDACTED_LAB_SECRET]" in texto or "security" in texto


def test_prepare_script_skip_campaigns() -> None:
    proc = subprocess.run(
        [sys.executable, str(RAIZ / "scripts" / "prepare_readme_demo.py"), "--skip-campaigns"],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0
