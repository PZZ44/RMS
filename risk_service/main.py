from fastapi import FastAPI
from schemas import RiskRequest, RiskResponse
from service import calculate_risk

app = FastAPI(title="Risk Service")


@app.post("/risk/calculate", response_model=RiskResponse)
def calculate(request: RiskRequest):
    result = calculate_risk(
        age=request.age,
        loyal_client=request.loyal_client,
        successful_loans_count=request.successful_loans_count
    )
    return result
