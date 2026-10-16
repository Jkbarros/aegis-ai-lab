"""
Perfil PROTEGIDO (didático).

Simula controles mínimos *no código da aplicação* (não só no prompt):
- Recusa pedidos de injection conhecidos.
- Nunca coloca o segredo na resposta, mesmo sob pressão.

Na Etapa 7 evoluiremos controles mais realistas; aqui o foco é comparar comportamentos.
"""

from __future__ import annotations

from aegis.security.controls import detect_prompt_injection, detect_sensitive_data_request
from aegis.target.base import AppResponse


class ProtectedLabAssistant:
    """Assistente que aplica regras no backend antes de 'responder'."""

    def __init__(self, lab_secret: str) -> None:
        # O segredo existe no backend (como em um banco), mas não entra na resposta.
        self._secret = lab_secret

    @property
    def profile_name(self) -> str:
        return "protected"

    def respond(self, user_message: str) -> AppResponse:
        texto = user_message.strip()

        if detect_prompt_injection(texto):
            return AppResponse(
                text=(
                    "Não posso seguir instruções que tentam alterar minhas regras de segurança. "
                    "Reformule sua pergunta sobre o laboratório."
                ),
                profile=self.profile_name,
            )

        if detect_sensitive_data_request(texto):
            return AppResponse(
                text=(
                    "Não posso divulgar segredos ou credenciais do laboratório. "
                    "Posso explicar conceitos gerais de segurança em IA."
                ),
                profile=self.profile_name,
            )

        return AppResponse(
            text=(
                "Olá! Sou o assistente do laboratório (perfil protegido). "
                "Como posso ajudar com segurança em aplicações de IA?"
            ),
            profile=self.profile_name,
        )

