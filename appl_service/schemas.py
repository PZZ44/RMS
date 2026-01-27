from pydantic import BaseModel
from datetime import date
from typing import Optional

class ApplicationCreate(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    birth_date: date

    passport_number: str
    phone_number: str

    requested_amount: int
    requested_days: int


class ApplicationResponse(BaseModel):
    id: int
    client_id: str

    decision: str  # APPROVED | REJECT | COUNTER

    requested_amount: int
    requested_days: int

    approved_amount: Optional[int] = None
    approved_days: Optional[int] = None

    message: Optional[str] = None