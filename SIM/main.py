from fastapi import FastAPI
from random import randint
from schemas import SIMRequest, SIMResponse

app = FastAPI(title="SIM Score Mock Service")


@app.post("/sim/score", response_model=SIMResponse)
def calculate_sim_score(request: SIMRequest):
    # Имитация телеком-скора:
    # ФИО, ДР и телефон используются как идентификаторы абонента

    return SIMResponse(
        lifetime=randint(0, 5),
        clc=randint(0, 5)
    )
