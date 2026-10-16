"""
Tipos compartilhados pela aplicação simulada.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AppResponse:
    """Resposta da aplicação avaliada + metadados úteis para o laboratório."""

    text: str
    profile: str


class LabAssistant(Protocol):
    """Contrato mínimo: qualquer 'app de IA' que o laboratório exercitar."""

    @property
    def profile_name(self) -> str:
        """Identificador da configuração (ex.: vulnerable, protected)."""

    def respond(self, user_message: str) -> AppResponse:
        """Processa a mensagem do usuário e devolve a resposta simulada."""
