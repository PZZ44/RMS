"""
Схемы данных SPR

Здесь описаны:
- входные данные от Application Service
- выходная модель SPR_Response

ВАЖНО:
- никаких вычислений
- только структура данных
"""

from pydantic import BaseModel
from typing import Optional


class ApplicationData(BaseModel):
    """
    Полная заявка клиента,
    сформированная Application Service
    """

    # === Идентификаторы ===
    id: int
    client_id: str

    # === Персональные данные (используются ТОЛЬКО для внешних запросов) ===
    first_name: str
    last_name: str
    middle_name: str
    birth_date: str  # YYYY-MM-DD

    phone_number: str
    passport_number: str  # с пробелом после серии

    # === Внутренние параметры клиента ===
    loyal_client: int  # 0 — новый, 1 — повторный
    successful_loans_count: int

    # === Пожелания клиента ===
    requested_amount: int
    requested_days: int


class SPR_Response(BaseModel):
    """
    Итоговое решение СПР
    """

    id: int
    client_id: str

    # Договор
    agr_number: Optional[str] = None   # ВВ-900/000015
    loan_num: Optional[int] = None      # номер займа по счёту

    # Итоговый скор
    final_score: int
    risk_band: Optional[str] = None

    
    # Итоговое решение
    #decision: str  # APPROVED / COUNTER / REJECT

    # Тип продукта (соответствует риск-банду)
    #product_type: Optional[str]

    # Запрошенные параметры
    requested_amount: int
    requested_days: int

    # Одобренные параметры
    approved_amount: int
    approved_days: int

    decision: str     # APPROVED / COUNTER / REJECT
    status: str        # OPEN / ISSUED / DECLINED / CLOSED

    # Причина отказа (если есть)
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