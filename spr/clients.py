"""
HTTP-клиенты для внешних сервисов

SPR не знает, КАК они реализованы —
он просто отправляет запрос и получает ответ
"""

import requests
from config import (
    RISK_SERVICE_URL,
    BKI_URL,
    SIM_URL,
    REQUEST_TIMEOUT
)


def call_risk_service(payload: dict) -> dict:
    """
    Вызов Risk Service

    Передаем:
    - возраст
    - лояльность
    - кол-во успешных займов
    """
    response = requests.post(
        RISK_SERVICE_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def call_bki(payload: dict) -> dict:
    """
    Вызов БКИ

    Передаем:
    - ФИО
    - дату рождения
    - паспорт
    """
    response = requests.post(
        BKI_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def call_sim(payload: dict) -> dict:
    """
    Вызов SIM (телеком скор)

    Передаем:
    - ФИО
    - дату рождения
    - телефон
    """
    response = requests.post(
        SIM_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()
