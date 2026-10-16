"""Demo Etapa 10 — executa o checklist de segurança."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def main() -> int:
    script = RAIZ / "scripts" / "check_security_lab.py"
    print("Rodando checklist de segurança...\n")
    return subprocess.call([sys.executable, str(script)], cwd=RAIZ)


if __name__ == "__main__":
    raise SystemExit(main())
