from dataclasses import dataclass

from src.engine.decision import form_decision
from src.engine.explain import explain
from src.engine.policy import Policy
from src.models.context import DecisionContext, DriftLevel, DriftMetrics, SystemState
from src.models.decisions import DecisionType


@dataclass(frozen=True)
class _FakeLLM:
    response: str

    def complete(self, prompt: str) -> str:
        return self.response


def _make_context():
    policy = Policy(name="default")
    decision = form_decision(
        decision_type=DecisionType.RECOMMEND,
        state=SystemState.PRESSURE,
        policy=policy,
        confidence=0.7,
    )
    return DecisionContext(
        decision=decision,
        drift_level=DriftLevel.SOFT_DRIFT,
        drift_metrics=DriftMetrics(magnitude=1.5, velocity=0.5, duration=4),
    )


def test_explanation_does_not_change_decision():
    context = _make_context()
    decision_before = context.decision

    result = explain(context, _FakeLLM(response="ok"))

    assert context.decision == decision_before
    assert result.decision_type == decision_before.decision_type
    assert result.state == decision_before.state
    assert result.policy_ref == decision_before.policy_ref


def test_explanation_text_is_external_only():
    context = _make_context()
    result = explain(context, _FakeLLM(response="alternate phrasing"))
    assert result.explanation == "alternate phrasing"
