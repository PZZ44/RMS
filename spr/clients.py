import requests
from config import (
    RISK_SERVICE_URL,
    BKI_URL,
    SIM_URL,
    REQUEST_TIMEOUT
)

def call_risk_service(payload: dict) -> dict:

    response = requests.post(
        RISK_SERVICE_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def call_bki(payload: dict) -> dict:

    response = requests.post(
        BKI_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def call_sim(payload: dict) -> dict:

    response = requests.post(
        SIM_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()
