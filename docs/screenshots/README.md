# Screenshots do portfólio

**Pasta oficial:** `docs/screenshots/` — salve aqui os PNG para o README e o LinkedIn.

Lista de nomes: [`ARQUIVOS-ESPERADOS.txt`](ARQUIVOS-ESPERADOS.txt).

## Preparar antes de capturar

```powershell
copy .env.demo .env
.\scripts\prepare_readme_demo.ps1
streamlit run app.py
```

Abra **http://127.0.0.1:8501** — veja [`README_DEMO.md`](../README_DEMO.md).

## Arquivos no repositório

| Arquivo | Página no menu |
|---------|----------------|
| `casos-de-teste.png` | Casos de Teste |
| `executar-testes.png` | Executar Testes |
| `resultados-caso.png` | Resultados |
| `conformidade-owasp.png` | Conformidade (OWASP) |
| `conformidade-mitre-attack.png` | Conformidade (MITRE ATT&CK) |
| `conformidade-mitre-atlas.png` | Conformidade (MITRE ATLAS) |
| `conformidade-nist.png` | Conformidade (NIST CSF) |

Resolução sugerida: largura ~1400px, tema escuro do app.

**Não inclua** na imagem: `.env`, chaves API ou segredos reais.

## Colar no README

Modelo pronto em [`README_DEMO.md`](../README_DEMO.md) (seção 5).
