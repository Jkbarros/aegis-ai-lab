"""
Teste mínimo da Etapa 1 (sem pytest por enquanto).

Execute na raiz do projeto: python tests/test_env.py

Quando você roda um arquivo dentro de tests/, o Python não inclui a raiz
do projeto automaticamente no caminho de importação. Por isso ajustamos
sys.path ao executar este arquivo diretamente (na Etapa 5 usaremos pytest
com configuração adequada).
"""

from __future__ import annotations

import sys
from pathlib import Path


def test_import_aegis() -> None:
    from aegis.lab import mensagem_boas_vindas, verificar_versao_python

    assert verificar_versao_python() is True
    assert "Aegis AI Lab" in mensagem_boas_vindas()


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(raiz))
    test_import_aegis()
    print("OK: tests/test_env.py passou.")
