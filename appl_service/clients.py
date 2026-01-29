import requests

SPR_URL = "http://spr:8001/spr"  

def call_spr(payload: dict) -> dict:
    response = requests.post(
        f"{SPR_URL}/decision",
        json=payload,
        timeout=5
    )
    if response.status_code != 200:
        print("SPR STATUS:", response.status_code)
        print("SPR RESPONSE:", response.text)
    response.raise_for_status()

    return response.json()

def call_spr_counter_accept(payload: dict) -> dict:
    response = requests.post(
        f"{SPR_URL}/counter/accept",
        json=payload,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def call_spr_counter_reject(payload: dict) -> dict:
    response = requests.post(
        f"{SPR_URL}/counter/reject",
        json=payload,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()