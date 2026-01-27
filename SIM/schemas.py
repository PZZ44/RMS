from pydantic import BaseModel
from datetime import date


class SIMRequest(BaseModel):
    last_name: str
    first_name: str
    middle_name: str | None = None
    birth_date: date
    phone_number: str


class SIMResponse(BaseModel):
    lifetime: int
    clc: int
