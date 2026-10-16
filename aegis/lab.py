"""
Ponto central do laboratório (será expandido nas próximas etapas).

Hoje: funções simples para validar que o pacote `aegis` está importável.
"""


def mensagem_boas_vindas() -> str:
    """Retorna uma mensagem fixa usada no programa de verificação da Etapa 1."""
    return (
        "Aegis AI Lab — ambiente Python configurado. "
        "Próximo passo: aplicação simulada vulnerável (Etapa 2)."
    )


def verificar_versao_python(minima: tuple[int, int, int] = (3, 10, 0)) -> bool:
    """
    Verifica se a versão do Python é suficiente para o projeto.

    Parâmetros:
        minima: tupla (major, minor, patch) mínima aceita.

    Retorno:
        True se a versão atual for >= minima; False caso contrário.
    """
    import sys

    atual = sys.version_info[:3]
    return atual >= minima
