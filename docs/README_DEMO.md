# Demo controlada para o README

Este guia monta um **ambiente previsível** para gravar tela ou tirar screenshots do Aegis AI Lab, sem expor credenciais e sem depender de OpenAI/Ollama (usa **apps simuladas**).

## 1. Preparar o ambiente (uma vez)

```powershell
cd "C:\Users\user\Documents\Projetos Cursor\Aegis AI Lab"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.demo .env
```

O arquivo [`.env.demo`](../.env.demo) deixa `OPENAI_API_KEY` vazio e usa um segredo **fictício** só para os casos de teste.

## 2. Gerar dados da demo

```powershell
.\scripts\prepare_readme_demo.ps1
```

Ou manualmente:

```powershell
python scripts\prepare_readme_demo.py --reset-reports --guided
```

Isso:

1. Executa campanhas `vulnerable`, `protected` e `hardened` (8 casos cada).
2. Salva relatórios sanitizados em `reports/`.
3. Copia versões fixas para [`docs/samples/`](samples/) (commitadas no Git para quem só lê o README).

## 3. Abrir o dashboard

```powershell
streamlit run app.py
```

Acesse: **http://127.0.0.1:8501** (não exponha na rede pública durante a gravação).

## 4. Capturas sugeridas

Salve em `docs/screenshots/` (PNG, tema escuro, janela ~1400px de largura).

| Arquivo | Onde clicar | O que mostrar |
|---------|-------------|----------------|
| `dashboard-overview.png` | **Dashboard** | Cartões + gráficos (dados reais após o passo 2) |
| `executar-testes.png` | **Executar Testes** | Perfil `hardened` + filtros |
| `resultados-caso.png` | **Resultados** | Um caso `pi-002` com veredito FAIL ou PASS |
| `conformidade.png` | **Conformidade** | Tabela OWASP / MITRE |
| `relatorios-comparacao.png` | **Relatórios** | Comparar vulnerable vs hardened |

**Não capture:** conteúdo do `.env`, chaves API, nem o valor bruto de `AEGIS_LAB_FAKE_SECRET`.

## 5. Incorporar no README

Depois de salvar as imagens, edite a seção **Screenshots** do [`README.md`](../README.md):

```markdown
## Demo visual

Ambiente controlado: `copy .env.demo .env` e `.\scripts\prepare_readme_demo.ps1`.

| Dashboard | Conformidade (OWASP / MITRE) |
|-----------|------------------------------|
| ![Dashboard](docs/screenshots/dashboard-overview.png) | ![Conformidade](docs/screenshots/conformidade.png) |

| Executar testes | Resultados |
|-----------------|------------|
| ![Executar](docs/screenshots/executar-testes.png) | ![Resultados](docs/screenshots/resultados-caso.png) |
```

### Amostras sem rodar o lab

Relatórios de exemplo (JSON sanitizado):

- [`docs/samples/campaign_demo_hardened.json`](samples/campaign_demo_hardened.json)
- [`docs/samples/campaign_demo_vulnerable.json`](samples/campaign_demo_vulnerable.json)

## 6. Vídeo curto (opcional)

Siga o roteiro de 5 min em [`DEMO.md`](DEMO.md). Comece pelo terminal (`pytest -q`) e depois o dashboard.

## Checklist antes de publicar

- [ ] `.env` não está no Git (`git status`)
- [ ] Screenshots sem dados pessoais
- [ ] `python -m pytest` passando
- [ ] `python scripts/check_security_lab.py` OK
