"""
Modelos de dados do laboratório (Etapa 3+).

Separamos:
- o que o teste espera (`EvaluationCriterion`),
- o que foi observado (`Observation`),
- o veredito final (`EvaluationVerdict`) com evidências auditáveis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Verdict(str, Enum):
    """Resultado da avaliação de um caso."""

    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
    INCONCLUSIVE = "INCONCLUSIVE"


class CriterionType(str, Enum):
    """Tipos de critério que o avaliador entende nesta etapa."""

    MUST_NOT_LEAK_SECRET = "must_not_leak_secret"
    MUST_NOT_CONTAIN = "must_not_contain"
    MUST_CONTAIN = "must_contain"


@dataclass(frozen=True)
class EvaluationCriterion:
    """
    Critério de avaliação definido pelo caso de teste.

    Exemplo (Etapa 2/3): MUST_NOT_LEAK_SECRET — o segredo fictício não pode aparecer na resposta.
    """

    type: CriterionType
    forbidden_substrings: tuple[str, ...] = ()
    required_substrings: tuple[str, ...] = ()
    case_sensitive: bool = False


@dataclass(frozen=True)
class Observation:
    """O que o laboratório observou ao executar o caso (entrada + resposta da app)."""

    user_input: str
    response_text: str
    profile: str = ""
    error_message: str | None = None


@dataclass(frozen=True)
class Evidence:
    """Prova objetiva usada para justificar o veredito."""

    code: str
    message: str
    snippet: str | None = None


@dataclass(frozen=True)
class EvaluationVerdict:
    """Veredito final + evidências (preservadas para relatório e revisão humana)."""

    status: Verdict
    criterion: CriterionType
    summary: str
    evidence: tuple[Evidence, ...] = field(default_factory=tuple)
