# Relatórios de demonstração

Arquivos gerados por `scripts/prepare_readme_demo.py` em **ambiente controlado**:

- Apps **simuladas** (sem chamada a OpenAI/Ollama)
- Segredo fictício `LAB-DEMO-CONTROLLED-ENV-ONLY`, redigido no JSON exportado
- Úteis para o README e para revisores que não querem rodar o lab imediatamente

Regenerar:

```powershell
python scripts\prepare_readme_demo.py --reset-reports
```
