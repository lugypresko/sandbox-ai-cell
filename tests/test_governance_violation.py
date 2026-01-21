import pytest
from src.governance.state_adapter import (
    GovernanceStateAdapter,
    GovernanceViolation,
)

def test_runtime_allows_progress_without_governance_enforcement():
    """
    This test proves that sustained PRESSURE violates
    Behavioral Safety Contract v1.2 and must be blocked.

    The system is DONE when this test PASSES
    by raising GovernanceViolation.
    """

    runtime_states = [
        "NORMAL",
        "DEGRADED",
        "PRESSURE",
        "PRESSURE",
        "PRESSURE",
    ]

    adapter = GovernanceStateAdapter()

    with pytest.raises(GovernanceViolation):
        for state in runtime_states:
            adapter.observe(state)
