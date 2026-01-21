from typing import Sequence

from pydantic import BaseModel, ConfigDict, Field

from ..models.context import DriftLevel, DriftMetrics
from ..models.signals import SignalPoint


DEFAULT_SOFT_MAGNITUDE = 1.0
DEFAULT_HARD_MAGNITUDE = 3.0
DEFAULT_SOFT_VELOCITY = 0.4
DEFAULT_HARD_VELOCITY = 1.2
DEFAULT_MIN_DURATION = 1


class DriftThresholds(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    soft_magnitude: float = Field(DEFAULT_SOFT_MAGNITUDE, ge=0)
    hard_magnitude: float = Field(DEFAULT_HARD_MAGNITUDE, ge=0)
    soft_velocity: float = Field(DEFAULT_SOFT_VELOCITY, ge=0)
    hard_velocity: float = Field(DEFAULT_HARD_VELOCITY, ge=0)
    min_duration: int = Field(DEFAULT_MIN_DURATION, ge=0)


def compute_drift(samples: Sequence[SignalPoint]) -> DriftMetrics:
    if len(samples) < 2:
        raise ValueError("at least two samples are required")

    first = samples[0]
    last = samples[-1]
    duration = last.timestamp - first.timestamp
    if duration < 0:
        raise ValueError("duration must be non-negative")

    magnitude = last.value - first.value
    velocity = magnitude / duration if duration > 0 else 0.0

    return DriftMetrics(magnitude=magnitude, velocity=velocity, duration=duration)


def classify_drift(metrics: DriftMetrics, thresholds: DriftThresholds) -> DriftLevel:
    if metrics.duration < thresholds.min_duration:
        return DriftLevel.NO_DRIFT

    magnitude = abs(metrics.magnitude)
    velocity = abs(metrics.velocity)

    if magnitude >= thresholds.hard_magnitude or velocity >= thresholds.hard_velocity:
        return DriftLevel.HARD_DRIFT
    if magnitude >= thresholds.soft_magnitude or velocity >= thresholds.soft_velocity:
        return DriftLevel.SOFT_DRIFT
    return DriftLevel.NO_DRIFT
