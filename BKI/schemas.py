from pydantic import BaseModel
from datetime import date
from typing import Optional


class BKIRequest(BaseModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    birth_date: str 
    passport_number: str  


class BKIResponse(BaseModel):
    bki_score: int
