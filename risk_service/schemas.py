from pydantic import BaseModel, Field


class RiskRequest(BaseModel):
    age: int = Field(..., ge=0, le=120)
    loyal_client: int = Field(..., ge=0, le=1)
    successful_loans_count: int = Field(..., ge=0, le=99)


class RiskResponse(BaseModel):
    base_score: int
    penalties: int
    final_score: int
    hard_reject: bool
    reject_reason: str | None = None
