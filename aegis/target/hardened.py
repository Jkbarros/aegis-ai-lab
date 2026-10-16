"""
Perfil HARDENED (Etapa 7) — controles em camadas no backend simulado.

Diferença em relação a `protected`:
- Usa o módulo `aegis.security` (validação + filtro de saída).
- Mensagens de bloqueio citam o ID do controle (auditoria didática).
"""

from __future__ import annotations

from aegis.security.controls import check_user_input, filter_model_output
from aegis.target.base import AppResponse


class HardenedLabAssistant:
    """App simulada com pipeline de segurança explícito."""

    def __init__(self, lab_secret: str) -> None:
        self._secret = lab_secret

    @property
    def profile_name(self) -> str:
        return "hardened"

    def respond(self, user_message: str) -> AppResponse:
        checagem = check_user_input(user_message)
        if not checagem.allowed:
            return AppResponse(
                text=(
                    "Não posso processar esta solicitação. "
                    f"(controle: {checagem.control_id}) "
                    f"{checagem.message}"
                ),
                profile=self.profile_name,
            )

        # Resposta genérica segura — o segredo nunca entra no texto gerado.
        corpo = (
            "Olá! Sou o assistente do laboratório (perfil hardened). "
            "Posso ajudar com conceitos de segurança em IA sem acessar dados internos."
        )
        corpo_filtrado, _ = filter_model_output(corpo, self._secret)
        return AppResponse(text=corpo_filtrado, profile=self.profile_name)
