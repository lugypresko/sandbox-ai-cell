from ..models.context import SystemState
from ..models.decisions import Decision, DecisionType
from .policy import Policy


def form_decision(
    decision_type: DecisionType,
    state: SystemState,
    policy: Policy,
    confidence: float,
) -> Decision:
    if not policy.allows(decision_type):
        raise PermissionError(f"decision type blocked by policy: {decision_type}")

    return Decision(
        decision_type=decision_type,
        state=state,
        policy_ref=policy.name,
        confidence=confidence,
    )
