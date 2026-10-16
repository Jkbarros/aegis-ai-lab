"""
Executor de casos de teste contra a aplicação avaliada (Etapa 4).

Fluxo: carregar caso -> enviar input à app simulada -> avaliar resposta -> comparar expectativa.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aegis.case_loader import TestCaseDefinition, load_all_cases, load_cases_file
from aegis.config import Settings, get_settings
from aegis.evaluator import Evaluator
from aegis.lab import criar_assistente
from aegis.models import EvaluationVerdict, Observation, Verdict
from aegis.target.base import LabAssistant


@dataclass(frozen=True)
class CaseExecutionResult:
    """Resultado completo de um caso executado contra um perfil."""

    case: TestCaseDefinition
    profile: str
    observation: Observation
    verdict: EvaluationVerdict
    expected_verdict: Verdict | None
    expectation_met: bool | None


@dataclass(frozen=True)
class CampaignSummary:
    """Resumo numérico de uma campanha (um perfil, vários casos)."""

    profile: str
    total: int
    passed: int
    failed: int
    errors: int
    inconclusive: int
    expectation_mismatches: int


class TestRunner:
    """Executa casos da biblioteca JSON contra um perfil da aplicação simulada."""

    def __init__(
        self,
        settings: Settings | None = None,
        evaluator: Evaluator | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._evaluator = evaluator or Evaluator()

    def run_case(self, case: TestCaseDefinition, profile: str) -> CaseExecutionResult:
        """Executa um único caso contra o perfil informado."""
        try:
            app = criar_assistente(profile, self._settings)
        except ValueError as exc:
            obs = Observation(
                user_input=case.user_input,
                response_text="",
                profile=profile,
                error_message=str(exc),
            )
            veredito = self._evaluator.evaluate(
                obs,
                case.evaluation,
                lab_secret=self._settings.lab_fake_secret,
            )
            return self._montar_resultado(case, profile, obs, veredito)

        return self._executar_em_app(case, app)

    def run_cases(
        self,
        cases: list[TestCaseDefinition],
        profile: str,
    ) -> list[CaseExecutionResult]:
        return [self.run_case(case, profile) for case in cases]

    def run_campaign(
        self,
        profile: str,
        directory: Path | None = None,
        *,
        categories: set[str] | None = None,
    ) -> list[CaseExecutionResult]:
        """
        Carrega casos do diretório e executa todos (ou filtra por risk_category).

        Parâmetros:
            profile: vulnerable ou protected.
            directory: pasta com JSON (padrão: test_cases/).
            categories: se informado, só executa casos cuja risk_category está no conjunto.
        """
        casos = load_all_cases(directory)
        if categories is not None:
            casos = [c for c in casos if c.risk_category in categories]
        return self.run_cases(casos, profile)

    def summarize(self, results: list[CaseExecutionResult]) -> CampaignSummary:
        if not results:
            return CampaignSummary(
                profile="",
                total=0,
                passed=0,
                failed=0,
                errors=0,
                inconclusive=0,
                expectation_mismatches=0,
            )

        perfil = results[0].profile
        passed = sum(1 for r in results if r.verdict.status == Verdict.PASS)
        failed = sum(1 for r in results if r.verdict.status == Verdict.FAIL)
        errors = sum(1 for r in results if r.verdict.status == Verdict.ERROR)
        inconclusive = sum(1 for r in results if r.verdict.status == Verdict.INCONCLUSIVE)
        mismatches = sum(1 for r in results if r.expectation_met is False)

        return CampaignSummary(
            profile=perfil,
            total=len(results),
            passed=passed,
            failed=failed,
            errors=errors,
            inconclusive=inconclusive,
            expectation_mismatches=mismatches,
        )

    def _executar_em_app(self, case: TestCaseDefinition, app: LabAssistant) -> CaseExecutionResult:
        try:
            saida = app.respond(case.user_input)
            obs = Observation(
                user_input=case.user_input,
                response_text=saida.text,
                profile=app.profile_name,
            )
        except Exception as exc:  # noqa: BLE001 — registramos como ERROR na avaliação
            obs = Observation(
                user_input=case.user_input,
                response_text="",
                profile=app.profile_name,
                error_message=f"Exceção na aplicação: {exc}",
            )

        veredito = self._evaluator.evaluate(
            obs,
            case.evaluation,
            lab_secret=self._settings.lab_fake_secret,
        )
        return self._montar_resultado(case, app.profile_name, obs, veredito)

    def _montar_resultado(
        self,
        case: TestCaseDefinition,
        profile: str,
        observation: Observation,
        verdict: EvaluationVerdict,
    ) -> CaseExecutionResult:
        esperado = case.expectations.get(profile)
        if esperado is None:
            met: bool | None = None
        else:
            met = verdict.status == esperado

        return CaseExecutionResult(
            case=case,
            profile=profile,
            observation=observation,
            verdict=verdict,
            expected_verdict=esperado,
            expectation_met=met,
        )


def load_cases_by_files(*nomes_arquivo: str) -> list[TestCaseDefinition]:
    """Atalho para carregar apenas alguns JSON pelo nome (ex.: 'prompt_injection.json')."""
    pasta = Path(__file__).resolve().parents[1] / "test_cases"
    casos: list[TestCaseDefinition] = []
    for nome in nomes_arquivo:
        casos.extend(load_cases_file(pasta / nome))
    return casos
