"""
Demonstração da Etapa 2 — vulnerable vs protected (sem LLM).

Execute na raiz do projeto:
  python scripts/demo_etapa2.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.config import get_settings
from aegis.lab import executar_demo_comparativa


def main() -> int:
    cfg = get_settings()

    print("=" * 70)
    print("Aegis AI Lab — Etapa 2: aplicação simulada")
    print("=" * 70)
    print(f"Segredo fictício (não é real): {cfg.lab_fake_secret[:20]}...")
    print()

    for item in executar_demo_comparativa(cfg):
        status = "VAZOU" if item.vazou_segredo else "OK"
        print(f"[{item.perfil:10}] [{status:5}] entrada: {item.entrada[:60]}{'...' if len(item.entrada) > 60 else ''}")
        print(f"             resposta: {item.resposta}")
        print()

    print("O que observar:")
    print("- vulnerable: injection e pedido direto de 'secret' tendem a VAZOU.")
    print("- protected: mesmas entradas devem permanecer OK (sem o segredo na resposta).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
