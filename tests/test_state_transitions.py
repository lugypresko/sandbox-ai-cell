from src.engine.state import StateMachine, StateMachineConfig
from src.models.context import DriftLevel, SystemState


def _make_machine():
    return StateMachine(
        StateMachineConfig(
            soft_persist=2,
            hard_persist=2,
            recovery_persist=2,
            normalize_persist=2,
        )
    )


def test_no_early_escalation_before_persistence():
    machine = _make_machine()
    machine.update(DriftLevel.HARD_DRIFT, index=0)
    machine.update(DriftLevel.HARD_DRIFT, index=1)
    assert machine.state == SystemState.DEGRADED

    machine.update(DriftLevel.HARD_DRIFT, index=2)
    machine.update(DriftLevel.HARD_DRIFT, index=3)
    assert machine.state == SystemState.PRESSURE


def test_recovery_requires_persistence_before_normal():
    machine = _make_machine()
    machine.update(DriftLevel.HARD_DRIFT, index=0)
    machine.update(DriftLevel.HARD_DRIFT, index=1)
    machine.update(DriftLevel.HARD_DRIFT, index=2)
    machine.update(DriftLevel.HARD_DRIFT, index=3)
    assert machine.state == SystemState.PRESSURE

    machine.update(DriftLevel.NO_DRIFT, index=4)
    assert machine.state == SystemState.PRESSURE

    machine.update(DriftLevel.NO_DRIFT, index=5)
    assert machine.state == SystemState.RECOVERY

    machine.update(DriftLevel.NO_DRIFT, index=6)
    assert machine.state == SystemState.RECOVERY

    machine.update(DriftLevel.NO_DRIFT, index=7)
    assert machine.state == SystemState.NORMAL


def test_degraded_must_pass_recovery_before_normal():
    machine = _make_machine()
    machine.update(DriftLevel.SOFT_DRIFT, index=0)
    machine.update(DriftLevel.SOFT_DRIFT, index=1)
    assert machine.state == SystemState.DEGRADED

    machine.update(DriftLevel.NO_DRIFT, index=2)
    assert machine.state == SystemState.DEGRADED

    machine.update(DriftLevel.NO_DRIFT, index=3)
    assert machine.state == SystemState.RECOVERY
