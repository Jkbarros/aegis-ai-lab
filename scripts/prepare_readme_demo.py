"""
Prepara ambiente controlado para demo do README / portfolio.

- Apps simuladas (sem OpenAI/Ollama obrigatorios)
- Campanhas vulnerable + protected + hardened
- Exporta relatorios de exemplo em docs/samples/ (versionados no Git)
- Opcional: limpa reports/ local e imprime roteiro de captura de tela

Uso:
  python scripts/prepare_readme_demo.py
  python scripts/prepare_readme_demo.py --guided
  python scripts/prepare_readme_demo.py --export-samples-only
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from aegis.config import Settings
from aegis.metrics import calcular_metricas
from aegis.reporter import PASTA_RELATORIOS, executar_e_salvar_campanha
from aegis.test_runner import TestRunner

_DEMO_SECRET = "LAB-DEMO-CONTROLLED-ENV-ONLY"
_SAMPLES = RAIZ / "docs" / "samples"


def _aplicar_env_demo() -> None:
    """Forca configuracao segura para gravacao (nao sobrescreve .env existente)."""
    os.environ.setdefault("LLM_PROVIDER", "openai")
    os.environ.setdefault("OPENAI_API_KEY", "")
    os.environ.setdefault("AEGIS_LAB_FAKE_SECRET", _DEMO_SECRET)


def _settings_demo() -> Settings:
    return Settings(
        llm_provider="openai",
        openai_api_key=None,
        openai_model="gpt-4o-mini",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="llama3.2",
        llm_timeout_seconds=60.0,
        lab_fake_secret=_DEMO_SECRET,
    )


def _limpar_reports_local() -> int:
    if not PASTA_RELATORIOS.is_dir():
        return 0
    removidos = 0
    for padrao in ("campaign_*.json", "campaign_*.md"):
        for arq in PASTA_RELATORIOS.glob(padrao):
            arq.unlink()
            removidos += 1
    return removidos


def _executar_campanhas(runner: TestRunner) -> dict[str, Path]:
    caminhos: dict[str, Path] = {}
    for perfil in ("vulnerable", "protected", "hardened"):
        _, path = executar_e_salvar_campanha(perfil, runner)
        caminhos[perfil] = path
        m = calcular_metricas(json.loads(path.read_text(encoding="utf-8")))
        print(
            f"  [{perfil}] salvo {path.name} | "
            f"FAIL {m.fail_rate:.0%} ({m.failed}/{m.total})"
        )
    return caminhos


def _exportar_samples(caminhos: dict[str, Path]) -> None:
    _SAMPLES.mkdir(parents=True, exist_ok=True)
    mapa_nomes = {
        "vulnerable": "campaign_demo_vulnerable.json",
        "protected": "campaign_demo_protected.json",
        "hardened": "campaign_demo_hardened.json",
    }
    for perfil, origem in caminhos.items():
        destino = _SAMPLES / mapa_nomes[perfil]
        shutil.copy2(origem, destino)
        md_origem = origem.with_suffix(".md")
        if md_origem.is_file():
            shutil.copy2(md_origem, destino.with_suffix(".md"))

    manifesto = {
        "description": "Relatorios sanitizados gerados em ambiente controlado (apps simuladas).",
        "secret_used": "[REDACTED - ficticio LAB-DEMO-CONTROLLED-ENV-ONLY]",
        "profiles": list(mapa_nomes.keys()),
        "files": list(mapa_nomes.values()),
    }
    (_SAMPLES / "manifest.json").write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nAmostras exportadas para {_SAMPLES.relative_to(RAIZ)}/")


def _roteiro_captura() -> None:
    print(
        """
=== Roteiro de captura (README) ===

1) Terminal (opcional):
   - Grave: python scripts/prepare_readme_demo.py
   - Ou: python -m pytest -q

2) Dashboard:
   streamlit run app.py
   URL: http://127.0.0.1:8501

3) Paginas para screenshot (salvar em docs/screenshots/):
   a) dashboard-overview.png     -> menu Dashboard
   b) executar-testes.png        -> Executar Testes (perfil hardened)
   c) resultados-caso.png        -> Resultados (expander com FAIL ou PASS)
   d) conformidade.png           -> Conformidade (tabela OWASP/MITRE)
   e) relatorios-comparacao.png  -> Relatorios (comparar vulnerable x hardened)

4) Antes de gravar:
   copy .env.demo .env
   (nao mostre .env na tela)

5) Atualize o README:
   docs/README_DEMO.md secao "Incorporar no README"

Detalhes: docs/README_DEMO.md
"""
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepara demo controlada para README")
    parser.add_argument(
        "--reset-reports",
        action="store_true",
        help="Remove campaign_*.json/.md em reports/ antes de executar",
    )
    parser.add_argument(
        "--export-samples-only",
        action="store_true",
        help="Regenera docs/samples/ a partir das campanhas (executa campanhas)",
    )
    parser.add_argument(
        "--guided",
        action="store_true",
        help="Mostra roteiro de captura de tela apos preparar",
    )
    parser.add_argument(
        "--skip-campaigns",
        action="store_true",
        help="Apenas imprime roteiro (nao executa campanhas)",
    )
    args = parser.parse_args()

    print("Aegis AI Lab — preparacao de demo controlada")
    print("=" * 50)
    _aplicar_env_demo()

    if args.skip_campaigns:
        if args.guided:
            _roteiro_captura()
        return 0

    if args.reset_reports:
        n = _limpar_reports_local()
        print(f"reports/ limpo ({n} arquivo(s) removidos).")

    runner = TestRunner(settings=_settings_demo())
    print("\nExecutando campanhas (apps simuladas, sem API externa)...")
    caminhos = _executar_campanhas(runner)
    _exportar_samples(caminhos)

    print("\nPronto. Abra o dashboard para capturas:")
    print("  streamlit run app.py")

    if args.guided or args.export_samples_only:
        _roteiro_captura()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
