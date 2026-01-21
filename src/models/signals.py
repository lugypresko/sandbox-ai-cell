from pydantic import BaseModel, ConfigDict, Field


class SignalPoint(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    timestamp: int = Field(..., ge=0)
    value: float
