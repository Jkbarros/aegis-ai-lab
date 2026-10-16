"""
Integrações com modelos de linguagem (OpenAI agora; Ollama na Etapa 6).

O restante do projeto deve depender da interface comum, não de um provedor específico.
"""

from aegis.llm.base import ChatMessage, LLMClient, LLMError
from aegis.llm.factory import create_llm_client

__all__ = [
    "ChatMessage",
    "LLMClient",
    "LLMError",
    "create_llm_client",
]
