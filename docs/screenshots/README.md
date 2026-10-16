# Screenshots do portfólio

## Preparar antes de capturar

```powershell
copy .env.demo .env
.\scripts\prepare_readme_demo.ps1
streamlit run app.py
```

Abra **http://127.0.0.1:8501** — veja [`README_DEMO.md`](../README_DEMO.md).

## Arquivos sugeridos

| Arquivo | Página no menu |
|---------|----------------|
| `dashboard-overview.png` | Dashboard |
| `executar-testes.png` | Executar Testes |
| `resultados-caso.png` | Resultados |
| `conformidade.png` | Conformidade |
| `relatorios-comparacao.png` | Relatórios |

Resolução sugerida: largura ~1400px, tema escuro do app.

**Não inclua** na imagem: `.env`, chaves API ou segredos reais.

## Colar no README

Modelo pronto em [`README_DEMO.md`](../README_DEMO.md) (seção 5).
