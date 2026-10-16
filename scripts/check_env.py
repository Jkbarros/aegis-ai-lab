"""Verificação do ambiente Python (antigo app.py CLI)."""

from __future__ import annotations

import sys

from aegis.lab import mensagem_boas_vindas, verificar_versao_python


def main() -> int:
    print("=" * 60)
    print("Aegis AI Lab — verificação do ambiente")
    print("=" * 60)
    versao = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Python em uso: {versao}")
    if not verificar_versao_python():
        print("ERRO: é necessário Python 3.10 ou superior.")
        return 1
    print("OK: versão do Python aceita.")
    print()
    print(mensagem_boas_vindas())
    print()
    print("Dashboard: streamlit run app.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
