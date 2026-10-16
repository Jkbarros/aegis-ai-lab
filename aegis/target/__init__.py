"""
Aplicação de IA *simulada* — alvo dos testes do laboratório.

Na Etapa 2 não usamos LLM real: funções Python imitam comportamentos
comuns (vazamento por obediência a injection vs resposta segura).
"""

from aegis.target.protected import ProtectedLabAssistant
from aegis.target.vulnerable import VulnerableLabAssistant

__all__ = ["ProtectedLabAssistant", "VulnerableLabAssistant"]
