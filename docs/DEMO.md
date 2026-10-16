# Roteiro de demonstração (~5 minutos)

Use este roteiro em entrevistas, vídeo de portfólio ou README. Tudo roda **local**; não é necessário expor chaves na gravação.

## Pré-requisitos (antes de gravar)

```powershell
cd "C:\Users\user\Documents\Projetos Cursor\Aegis AI Lab"
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Opcional: LLM_PROVIDER=ollama e Ollama rodando
python scripts\check_env.py
```

## Linha do tempo

| Tempo | O que mostrar | Comando / ação |
|-------|----------------|----------------|
| **0:00–0:45** | Problema e escopo | Explicar: lab para **testar apps com LLM** (injection, vazamento), só alvos autorizados. Abrir [`docs/SECURITY.md`](SECURITY.md) por 10 s. |
| **0:45–1:30** | Qualidade automatizada | `python -m pytest -q` e `python scripts\check_security_lab.py` |
| **1:30–2:30** | Campanha no terminal | `python scripts\demo_etapa11.py` (vulnerable vs hardened) |
| **2:30–4:00** | Dashboard | `streamlit run app.py` → **Executar Testes** (perfil `hardened`) → **Resultados** → evidências |
| **4:00–4:45** | Métricas e relatório | Aba **Relatórios** → comparar campanhas → download Markdown |
| **4:45–5:00** | Fechamento | Arquitetura em [`ARCHITECTURE.md`](ARCHITECTURE.md); link do GitHub |

## Falas sugeridas (curtas)

1. *"Os casos vivem em JSON versionado; o avaliador não é uma caixa preta — cada FAIL traz critério e evidência."*
2. *"Três perfis simulam maturidade da aplicação: vulnerável, protegida e hardened."*
3. *"Relatórios são sanitizados antes de ir para `reports/`, para não vazar segredo do `.env`."*

## Atalho único

```powershell
python scripts\demo_etapa11.py --full
```

Depois abra o dashboard manualmente (`streamlit run app.py`) se estiver gravando tela.

## Screenshots para o README

Capture e salve em `docs/screenshots/` (veja `docs/screenshots/README.md`).
