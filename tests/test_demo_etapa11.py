"""Smoke test do script de demo (Etapa 11)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def test_demo_etapa11_skip_campaigns() -> None:
    proc = subprocess.run(
        [sys.executable, str(RAIZ / "scripts" / "demo_etapa11.py"), "--skip-campaigns"],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0
    assert "docs/DEMO.md" in proc.stdout
