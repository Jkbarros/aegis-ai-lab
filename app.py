"""
Ponto de entrada do Aegis AI Lab (interface futura via Streamlit na Etapa 8).

Na Etapa 1, este arquivo só confirma que o ambiente e o pacote `aegis` funcionam.
Execute com: python app.py
"""

from __future__ import annotations

import sys

from aegis.lab import mensagem_boas_vindas, verificar_versao_python


def main() -> int:
    """
    Executa verificações básicas e imprime o status.

    Retorno:
        0 se tudo ok; 1 se alguma verificação falhar.
    """
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
    print("Próximo passo didático: python scripts/demo_etapa4.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
