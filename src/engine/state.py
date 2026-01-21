from pydantic import BaseModel, ConfigDict, Field

from ..models.context import DriftLevel, StateTransition, SystemState


class StateMachineConfig(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    soft_persist: int = Field(..., ge=1)
    hard_persist: int = Field(..., ge=1)
    recovery_persist: int = Field(..., ge=1)
    normalize_persist: int = Field(..., ge=1)


class StateMachine:
    def __init__(
        self,
        config: StateMachineConfig,
        initial_state: SystemState = SystemState.NORMAL,
    ) -> None:
        self._config = config
        self._state = initial_state
        self._soft_count = 0
        self._hard_count = 0
        self._no_drift_count = 0

    @property
    def state(self) -> SystemState:
        return self._state

    def update(self, drift_level: DriftLevel, index: int) -> StateTransition | None:
        self._update_counts(drift_level)

        if self._state == SystemState.NORMAL:
            if self._soft_count >= self._config.soft_persist:
                return self._transition(SystemState.DEGRADED, index, "soft_drift_persist")

        elif self._state == SystemState.DEGRADED:
            if self._hard_count >= self._config.hard_persist:
                return self._transition(SystemState.PRESSURE, index, "hard_drift_persist")
            if self._no_drift_count >= self._config.recovery_persist:
                return self._transition(SystemState.RECOVERY, index, "recovery_persist")

        elif self._state == SystemState.PRESSURE:
            if self._no_drift_count >= self._config.recovery_persist:
                return self._transition(SystemState.RECOVERY, index, "recovery_persist")

        elif self._state == SystemState.RECOVERY:
            if self._no_drift_count >= self._config.normalize_persist:
                return self._transition(SystemState.NORMAL, index, "normalize_persist")
            if self._soft_count >= self._config.soft_persist:
                return self._transition(SystemState.DEGRADED, index, "soft_drift_persist")

        return None

    def _update_counts(self, drift_level: DriftLevel) -> None:
        if drift_level == DriftLevel.NO_DRIFT:
            self._no_drift_count += 1
            self._soft_count = 0
            self._hard_count = 0
            return

        if drift_level == DriftLevel.SOFT_DRIFT:
            self._soft_count += 1
            self._hard_count = 0
            self._no_drift_count = 0
            return

        if drift_level == DriftLevel.HARD_DRIFT:
            self._soft_count += 1
            self._hard_count += 1
            self._no_drift_count = 0
            return

        raise ValueError(f"unknown drift level: {drift_level}")

    def _transition(
        self,
        new_state: SystemState,
        index: int,
        reason: str,
    ) -> StateTransition:
        transition = StateTransition(
            from_state=self._state,
            to_state=new_state,
            at_index=index,
            reason=reason,
        )
        self._state = new_state
        self._soft_count = 0
        self._hard_count = 0
        self._no_drift_count = 0
        return transition
