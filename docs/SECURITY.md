# Segurança do Aegis AI Lab (Etapa 10)

Este documento descreve o **escopo seguro de uso** do laboratório e as decisões
de proteção do próprio projeto.

## Escopo autorizado

- Testar apenas **aplicações simuladas** incluídas no repositório (`aegis/target/`) ou
  assistentes locais que **você** configurou (Ollama/OpenAI com suas credenciais).
- Executar em **máquina local** ou ambiente de desenvolvimento sob seu controle.
- Usar casos de teste versionados em `test_cases/` — não apontar o lab para URLs ou
  APIs de terceiros sem autorização explícita.

## Fora de escopo (não faça)

- Varredura, prompt injection ou exfiltração contra sistemas que você não possui ou
  não tem permissão escrita para testar.
- Publicar relatórios em `reports/` contendo dados reais de produção, PII ou chaves.
- Expor o dashboard Streamlit na internet sem autenticação e revisão de risco.

## Segredos e configuração

| Item | Onde fica | Versionado no Git? |
|------|-----------|-------------------|
| `OPENAI_API_KEY` | `.env` | **Não** |
| `AEGIS_LAB_FAKE_SECRET` | `.env` (segredo **fictício** para casos de teste) | **Não** |
| `.env.example` | Raiz | Sim (sem valores reais) |

O dashboard mostra apenas **se** a chave OpenAI está configurada (`true`/`false`), nunca o valor.

## Relatórios (`reports/`)

Antes de gravar JSON/Markdown, o lab aplica **sanitização**:

- Substitui o valor de `AEGIS_LAB_FAKE_SECRET` por `[REDACTED_LAB_SECRET]`.
- Mascara padrões de chave OpenAI (`sk-...`).
- Não inclui `openai_api_key` no bloco `lab` do relatório.

Vereditos **FAIL** por vazamento continuam válidos; evidências usam códigos (`secret_full_match`)
sem repetir o segredo do `.env`.

## Dashboard Streamlit

- Por padrão, use `streamlit run app.py` em **localhost** (`127.0.0.1`).
- Configuração em `.streamlit/config.toml` evita escutar em todas as interfaces sem necessidade.
- Não há login embutido: quem acessa a URL vê campanhas e relatórios locais.

## Dependências

```powershell
pip install -r requirements.txt
pip audit
```

Revise avisos do `pip audit` e atualize pacotes quando fizer sentido para o seu ambiente.

## Verificação automatizada

```powershell
python scripts/check_security_lab.py
python -m pytest tests/test_security_lab.py
```

## Mapeamento a frameworks (OWASP / MITRE / NIST)

O laboratório inclui tags didáticas por caso de teste. Isso **não** substitui auditoria formal.
Veja [`COMPLIANCE.md`](COMPLIANCE.md).

## Limitações honestas

- Heurísticas de injection e redação **não** substituem revisão humana nem pentest completo.
- Modelos LLM reais são não determinísticos; perfis simulados são mais reproduzíveis.
- O Aegis é um **projeto pedagógico de portfólio**, não um produto certificado.

## Reportar problemas

Se encontrar um vazamento de segredo em relatório ou na UI após sanitização, abra uma issue
no repositório (sem colar chaves reais na descrição).
