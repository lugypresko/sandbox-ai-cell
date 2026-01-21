from pydantic import BaseModel, ConfigDict, Field

from ..models.decisions import DecisionType


class Policy(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    name: str = Field(..., min_length=1)
    allow_act: bool = False
    allow_recommend: bool = True
    allow_none: bool = True

    def allows(self, decision_type: DecisionType) -> bool:
        if decision_type == DecisionType.ACT:
            return self.allow_act
        if decision_type == DecisionType.RECOMMEND:
            return self.allow_recommend
        if decision_type == DecisionType.NONE:
            return self.allow_none
        raise ValueError(f"unknown decision type: {decision_type}")
