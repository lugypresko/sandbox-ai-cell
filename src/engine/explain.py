from typing import Protocol

from ..models.context import DecisionContext
from ..models.explanations import Explanation


class LLMClient(Protocol):
    def complete(self, prompt: str) -> str:
        ...


def explain(decision_context: DecisionContext, llm: LLMClient) -> Explanation:
    prompt = _build_prompt(decision_context)
    text = llm.complete(prompt)
    return Explanation(
        decision_type=decision_context.decision.decision_type,
        state=decision_context.decision.state,
        policy_ref=decision_context.decision.policy_ref,
        explanation=text,
    )


def _build_prompt(decision_context: DecisionContext) -> str:
    decision = decision_context.decision
    metrics = decision_context.drift_metrics
    return (
        "Explain the decision in plain terms.\n"
        f"decision_type: {decision.decision_type}\n"
        f"state: {decision.state}\n"
        f"policy_ref: {decision.policy_ref}\n"
        f"confidence: {decision.confidence}\n"
        f"drift_level: {decision_context.drift_level}\n"
        f"drift_magnitude: {metrics.magnitude}\n"
        f"drift_velocity: {metrics.velocity}\n"
        f"drift_duration: {metrics.duration}\n"
        "Constraints:\n"
        "- Explain, do not decide.\n"
        "- Do not infer policy details beyond policy_ref.\n"
        "- Do not suggest actions.\n"
    )
