Aegis AI Lab — casos de teste JSON (exemplos didáticos)

Arquivos:
- prompt_injection.json: perguntas normais e tentativas de prompt injection.
- data_exposure.json: casos para verificar se um segredo fictício é exposto.

Importante:
- Estes são exemplos criados para o projeto, não um dataset oficial.
- O segredo LAB-SECRET-4821 é fictício; não substitua por senhas ou segredos reais.
- expected_status representa o resultado esperado, mas o seu runner precisa carregar os JSONs,
  executar cada prompt e comparar o resultado real com o esperado.
- Os status esperados pressupõem que um teste bem-sucedido de segurança não revele o segredo.
  Ajuste o mapeamento se seu avaliador usar nomes de status diferentes.
- A sintaxe JSON pode ser validada com:
  python -m json.tool .\test_cases\prompt_injection.json
  python -m json.tool .\test_cases\data_exposure.json

Converter para o formato do Aegis (raiz test_cases/):
  python scripts\convert_aegis_json_import.py
  -> gera test_cases\import_aegis_json.json
