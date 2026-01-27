from fastapi import FastAPI
from random import randint
from schemas import BKIRequest, BKIResponse

app = FastAPI(title="BKI Mock Service")


@app.post("/bki/score", response_model=BKIResponse)
def calculate_bki_score(request: BKIRequest):
    # Имитация БКИ:
    # в реальности данные используются для поиска истории,
    # здесь — просто валидируются схемой

    return BKIResponse(
        bki_score=randint(400, 750)
    )
