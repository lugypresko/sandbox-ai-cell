from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class DriftLevel(str, Enum):
    NO_DRIFT = "NO_DRIFT"
    SOFT_DRIFT = "SOFT_DRIFT"
    HARD_DRIFT = "HARD_DRIFT"


class SystemState(str, Enum):
    NORMAL = "NORMAL"
    DEGRADED = "DEGRADED"
    PRESSURE = "PRESSURE"
    RECOVERY = "RECOVERY"


class DriftMetrics(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    magnitude: float
    velocity: float
    duration: int = Field(..., ge=0)


class StateTransition(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    from_state: SystemState
    to_state: SystemState
    at_index: int = Field(..., ge=0)
    reason: str


class DecisionContext(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    decision: "Decision"
    drift_level: DriftLevel
    drift_metrics: DriftMetrics


from .decisions import Decision  # noqa: E402
