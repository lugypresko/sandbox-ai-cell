from src.engine.buffer import EvidenceBuffer
from src.engine.drift import DriftThresholds, classify_drift, compute_drift
from src.engine.state import StateMachine, StateMachineConfig
from src.models.signals import SignalPoint


def _run_sequence(values):
    buffer = EvidenceBuffer(maxlen=3)
    thresholds = DriftThresholds()
    config = StateMachineConfig(
        soft_persist=2,
        hard_persist=2,
        recovery_persist=2,
        normalize_persist=2,
    )
    machine = StateMachine(config)

    states = []
    transitions = []
    for idx, value in enumerate(values):
        buffer.add(SignalPoint(timestamp=idx, value=value))
        if len(buffer) < 2:
            states.append(machine.state)
            continue
        metrics = compute_drift(buffer.samples())
        drift_level = classify_drift(metrics, thresholds)
        transition = machine.update(drift_level, index=idx)
        states.append(machine.state)
        if transition:
            transitions.append(transition.model_dump())
    return states, transitions


def test_same_sequence_same_transition_timing():
    values = [0.0, 0.5, 1.1, 2.0, 2.8, 3.6, 3.6, 3.6]
    states_a, transitions_a = _run_sequence(values)
    states_b, transitions_b = _run_sequence(values)

    assert states_a == states_b
    assert transitions_a == transitions_b
