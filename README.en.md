# Aegis AI Lab

**English** | [Português](README.md)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

A local lab for **security assessment** of LLM-powered applications: *prompt injection*, data exposure, defense validation, and metric-backed reports — with **simulated** apps and an optional LLM (Ollama/OpenAI).

> **Ethical use:** only on systems you own or with explicit authorization. See [`docs/SECURITY.md`](docs/SECURITY.md).

**Repository:** [github.com/Jkbarros/aegis-ai-lab](https://github.com/Jkbarros/aegis-ai-lab)

---

## Highlights

- Versioned test cases in JSON (`test_cases/`) with risk levels and expectations.
- `vulnerable`, `protected`, and `hardened` profiles to compare application maturity.
- Evaluator with explicit criteria (PASS/FAIL/INCONCLUSIVE) and traceable evidence.
- Streamlit dashboard styled as a *security command center* (local, `127.0.0.1`).
- Reports using schema **1.1** (metrics, recommendations, sanitized JSON + Markdown).
- Per-case mapping to **OWASP LLM**, **MITRE ATT&CK**, **MITRE ATLAS**, and **NIST CSF 2.0**.
- **16** test cases (8 official + JSON import) and **60** `pytest` tests.

## Visual demo (controlled environment)

**No API keys:** copy [`.env.demo`](.env.demo) to `.env` and run the preparer — it runs three simulated campaigns and leaves the dashboard ready for screenshots.

```powershell
copy .env.demo .env
.\scripts\prepare_readme_demo.ps1
streamlit run app.py
```

Full guide (captures, checklist, markdown for the README): **[`docs/README_DEMO.md`](docs/README_DEMO.md)** (Portuguese).

Sample versioned reports (sanitized): [`docs/samples/`](docs/samples/).

### Screenshots

| Test cases (16) | Run campaign |
|-----------------|--------------|
| ![Test cases](docs/screenshots/casos-de-teste.png) | ![Run tests](docs/screenshots/executar-testes.png) |

| Results | Compliance (OWASP LLM) |
|---------|-------------------------|
| ![Results](docs/screenshots/resultados-caso.png) | ![OWASP compliance](docs/screenshots/conformidade-owasp.png) |

<details>
<summary>More captures — frameworks (MITRE / NIST)</summary>

| MITRE ATT&CK | MITRE ATLAS |
|--------------|-------------|
| ![MITRE ATT&CK](docs/screenshots/conformidade-mitre-attack.png) | ![MITRE ATLAS](docs/screenshots/conformidade-mitre-atlas.png) |

![NIST CSF 2.0](docs/screenshots/conformidade-nist.png)

</details>

More files and names: [`docs/screenshots/`](docs/screenshots/).

## Quick start

```powershell
git clone https://github.com/Jkbarros/aegis-ai-lab.git
cd aegis-ai-lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python scripts\check_env.py
python -m pytest
streamlit run app.py
```

Portfolio demo (~5 min):

```powershell
.\scripts\run_demo.ps1
# or
python scripts\demo_etapa11.py --full
```

Narrated walkthrough: [`docs/DEMO.md`](docs/DEMO.md) (Portuguese).

## Architecture

```mermaid
flowchart LR
    JSON[test_cases] --> Runner[TestRunner]
    Runner --> App[Simulated profiles]
    Runner --> Eval[Evaluator]
    Eval --> Report[Reporter + Metrics]
    Report --> Disk[(reports/)]
    UI[Streamlit] --> Runner
```

Details: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Compliance and frameworks

Test cases reference controls and techniques in [`docs/COMPLIANCE.md`](docs/COMPLIANCE.md).
Catalog: `aegis/compliance/framework_catalog.json`. Campaign coverage in the dashboard (**Compliance**) and in reports (`compliance_coverage`).

## Project structure

```
aegis/
  case_loader.py      # JSON cases
  test_runner.py      # Campaigns
  evaluator.py        # Criteria and verdicts
  reporter.py         # Persistence
  metrics.py          # Rates and comparison
  security/           # Controls + report sanitization
  target/             # Simulated apps + LLM assistants
  llm/                # Ollama / OpenAI
  dashboard*.py       # Streamlit UI
test_cases/           # Security scenarios
tests/                # pytest
docs/                 # SECURITY, ARCHITECTURE, DEMO
scripts/              # Verification, staged demos
```

## Configuration

| Variable | Description |
|----------|-------------|
| `LLM_PROVIDER` | `ollama` or `openai` |
| `OLLAMA_MODEL` | e.g. `llama3.2` |
| `OPENAI_API_KEY` | optional; only in `.env` |
| `AEGIS_LAB_FAKE_SECRET` | **fictional** secret for leakage scenarios |

```powershell
python scripts\verify_ollama.py --ping
python scripts\verify_openai.py --ping
```

## Documentation by stage (learning path)

| Stage | Topic |
|-------|--------|
| 1–4 | Structure, simulated apps, evaluator, JSON cases |
| 5 | `pytest` |
| 6 | Ollama / OpenAI |
| 7 | `hardened` controls |
| 8–9 | Dashboard and metrics |
| 10 | [`docs/SECURITY.md`](docs/SECURITY.md) |
| 11 | This README, [`docs/DEMO.md`](docs/DEMO.md), demo script |

## Security and quality

```powershell
python scripts\check_security_lab.py
pip audit
python -m pytest
```

## License

MIT — see [`LICENSE`](LICENSE).

## Author

**Julio** — portfolio project in AI application security.

Commits in the repository are made by the maintainer; see [`.cursor/rules/git-commits-usuario.mdc`](.cursor/rules/git-commits-usuario.mdc).
