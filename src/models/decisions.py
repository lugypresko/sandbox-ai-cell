from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .context import SystemState


class DecisionType(str, Enum):
    NONE = "NONE"
    RECOMMEND = "RECOMMEND"
    ACT = "ACT"


class Decision(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    decision_type: DecisionType
    state: SystemState
    policy_ref: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
