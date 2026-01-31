from pydantic import BaseModel
from typing import Optional


class ApplicationData(BaseModel):

    id: int
    client_id: str

    first_name: str
    last_name: str
    middle_name: str
    birth_date: str 

    phone_number: str
    passport_number: str 

    loyal_client: int  # 0 — новый, 1 — повторный
    successful_loans_count: int

    requested_amount: int
    requested_days: int


class SPR_Response(BaseModel):

    id: int
    client_id: str

    agr_number: Optional[str] = None   # ВВ-900/000015
    loan_num: Optional[int] = None      # номер займа по счёту

    final_score: int
    risk_band: Optional[str] = None

    requested_amount: int
    requested_days: int

    approved_amount: int
    approved_days: int

    decision: str     # APPROVED / COUNTER / REJECT
    status: str        # OPEN / ISSUED / DECLINED / CLOSED
    reject_reason: Optional[str]



class CounterActionRequest(BaseModel):
    id: int
    reason: str | None = None


class CounterActionResponse(BaseModel):
    id: int
    decision: str
    approved_amount: int | None = None
    approved_days: int | None = None
    agr_number: str | None = None
    reject_reason: str | None = None