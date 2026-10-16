"""
Perfil PROTEGIDO (didático).

Simula controles mínimos *no código da aplicação* (não só no prompt):
- Recusa pedidos de injection conhecidos.
- Nunca coloca o segredo na resposta, mesmo sob pressão.

Na Etapa 7 evoluiremos controles mais realistas; aqui o foco é comparar comportamentos.
"""

from __future__ import annotations

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
        lower = texto.lower()

        if self._parece_tentativa_de_injection(lower):
            return AppResponse(
                text=(
                    "Não posso seguir instruções que tentam alterar minhas regras de segurança. "
                    "Reformule sua pergunta sobre o laboratório."
                ),
                profile=self.profile_name,
            )

        if self._pede_dado_sensivel(lower):
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

    def _parece_tentativa_de_injection(self, lower_message: str) -> bool:
        gatilhos_ignorar = ("ignore", "disregard", "forget", "ignorar", "esqueça")
        gatilhos_contexto = ("instruction", "instru", "previous", "anterior", "regras", "system")
        tem_ignorar = any(g in lower_message for g in gatilhos_ignorar)
        tem_contexto = any(g in lower_message for g in gatilhos_contexto)
        return tem_ignorar and tem_contexto

    def _pede_dado_sensivel(self, lower_message: str) -> bool:
        return any(
            palavra in lower_message
            for palavra in ("segredo", "secret", "password", "senha", "api key", "chave")
        )
