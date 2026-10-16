# Aegis AI Lab

Laboratório local para testes de segurança em aplicações que usam modelos de linguagem (LLMs).

**Status:** Etapa 5 — testes automatizados com pytest.

Use apenas em aplicações próprias, modelos locais e ambientes autorizados.

## Repositório GitHub

Após o primeiro commit **feito por você**, o remoto sugerido é:

`https://github.com/Jkbarros/aegis-ai-lab`

## Configuração OpenAI (opcional nesta etapa)

1. Copie o exemplo de variáveis:

   ```powershell
   copy .env.example .env
   ```

2. Edite `.env` e defina `OPENAI_API_KEY` (nunca commite este arquivo).

3. Instale dependências e verifique:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python scripts\verify_openai.py
   python scripts\verify_openai.py --ping
   ```

O módulo `aegis/llm/` abstrai o provedor (OpenAI e Ollama).

## Ollama + Llama 3.2 (Etapa 6)

No `.env`:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

Verificação (usa a API HTTP — **não** precisa do comando `ollama` no PATH):

```powershell
python scripts\verify_ollama.py --ping
python scripts\demo_etapa6_ollama.py --case pi-001
```

### Comando `ollama` não reconhecido no terminal do Cursor

O instalador adiciona o Ollama ao PATH do **usuário**, mas terminais já abertos (ou o Cursor) podem não recarregar isso.

**Opção A — recarregar PATH na sessão:**

```powershell
.\scripts\refresh-path.ps1
ollama list
```

**Opção B — atalho do projeto (sempre funciona):**

```powershell
.\scripts\ollama.ps1 list
.\scripts\ollama.ps1 run llama3.2 "Ola"
```

**Opção C — caminho completo:**

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" list
```

## Política de commits

Todos os commits são feitos **manualmente pelo mantenedor do projeto**. A IA do Cursor pode editar arquivos, mas não deve criar commits em seu nome (regra em `.cursor/rules/git-commits-usuario.mdc`).

Confira seu autor Git antes do primeiro commit:

```powershell
git config user.name
git config user.email
```

Se estiver vazio, configure **você mesmo** (exemplo):

```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

## Testes automatizados (Etapa 5)

```powershell
cd "C:\Users\user\Documents\Projetos Cursor\Aegis AI Lab"
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
```

Atalho no PowerShell:

```powershell
.\scripts\run_tests.ps1
```

Só testes de integração (campanha completa):

```powershell
python -m pytest -m integration
```

## Execução rápida

```powershell
python app.py
python scripts\demo_etapa4.py
```
