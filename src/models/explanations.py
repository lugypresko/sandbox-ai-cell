from pydantic import BaseModel, ConfigDict, Field

from .decisions import DecisionType
from .context import SystemState


class Explanation(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    decision_type: DecisionType
    state: SystemState
    policy_ref: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=1)
