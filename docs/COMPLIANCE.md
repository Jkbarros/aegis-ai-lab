# Frameworks de segurança (OWASP, MITRE, NIST)

O Aegis AI Lab **mapeia casos de teste** a referências amplamente usadas em cibersegurança.
Isso ajuda a comunicar risco para gestores e times AppSec — **não** equivale a conformidade
certificada ou assessment oficial.

## Frameworks suportados

| Framework | Uso no lab | Catálogo |
|-----------|------------|----------|
| **OWASP Top 10 for LLM Applications** | Riscos específicos de apps com LLM (ex.: LLM01 Injection, LLM02 Disclosure) | `aegis/compliance/framework_catalog.json` |
| **MITRE ATT&CK (Enterprise)** | Técnicas analogas (ex.: phishing / conteúdo enganoso para injection indireta) | idem |
| **MITRE ATLAS** | Ataques a sistemas de ML/LLM (ex.: AML.T0051 Prompt Injection) | idem |
| **NIST Cybersecurity Framework 2.0** | Funções/categorias (PR.DS, DE.CM, RS.MA, GV.OC) | idem |

## Onde aparece no produto

1. **JSON de casos** — campo opcional `compliance` por caso em `test_cases/*.json`.
2. **Relatórios** — bloco `compliance_coverage` após cada campanha (JSON/Markdown).
3. **Dashboard** — menu **Conformidade** (catálogo + cobertura da última execução).

## Como adicionar mapeamento a um caso

```json
"compliance": {
  "owasp_llm": ["LLM01"],
  "mitre_attack": ["T1566"],
  "mitre_atlas": ["AML.T0051"],
  "nist_csf": ["PR.DS", "DE.CM"]
}
```

Se `compliance` estiver ausente, o lab aplica **defaults por `risk_category`**
(`prompt_injection`, `data_exposure`).

## Interpretação dos resultados

- **FAIL** em um caso conta como gap nos controles/técnicas mapeados — sinal para correção ou mitigação.
- **PASS** indica que, para aquele cenário sintético, a aplicação atendeu ao critério do avaliador.
- Controles NIST listados descrevem **onde o teste se encaixa no ciclo de gestão de risco**, não que a organização “implementou NIST” por completo.

## Limitações

- Cobertura limitada aos casos versionados no repositório.
- MITRE ATT&CK Enterprise não foi desenhado só para LLM; usamos mapeamento **ilustrativo**.
- Para produção, combine este lab com threat modeling, revisão de código e políticas da sua organização.

## Referências

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST CSF 2.0](https://www.nist.gov/cyberframework)
