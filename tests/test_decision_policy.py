import pytest

from src.engine.decision import form_decision
from src.engine.policy import Policy
from src.models.context import SystemState
from src.models.decisions import DecisionType


def test_policy_blocks_act_by_default():
    policy = Policy(name="default")
    with pytest.raises(PermissionError):
        form_decision(
            decision_type=DecisionType.ACT,
            state=SystemState.PRESSURE,
            policy=policy,
            confidence=0.7,
        )


def test_decision_is_explicit_and_deterministic():
    policy = Policy(name="default")
    decision_a = form_decision(
        decision_type=DecisionType.RECOMMEND,
        state=SystemState.PRESSURE,
        policy=policy,
        confidence=0.7,
    )
    decision_b = form_decision(
        decision_type=DecisionType.RECOMMEND,
        state=SystemState.PRESSURE,
        policy=policy,
        confidence=0.7,
    )

    assert decision_a == decision_b
