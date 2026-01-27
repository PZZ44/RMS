from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import ApplicationData, SPR_Response
from service import make_decision
from counter_service import accept_counter, reject_counter
from schemas import CounterActionRequest, CounterActionResponse

app = FastAPI(title="SPR Decision Service")


@app.post("/spr/decision", response_model=SPR_Response)
def spr_decision(
    data: ApplicationData,
    db: Session = Depends(get_db),
):
    spr, decision = make_decision(db, data)

    return SPR_Response(
        id=spr.id,
        client_id=spr.client_id,
        agr_number=spr.agr_number,
        loan_num=spr.loan_num,
        final_score=spr.final_score,
        risk_band=spr.risk_band,
        decision=spr.decision,
        status=spr.status,
        #product_type=spr.risk_band if decision != "REJECT" else None,
        requested_amount=data.requested_amount,
        requested_days=data.requested_days,
        approved_amount=spr.approved_amount or 0,
        approved_days=spr.approved_days or 0,
        reject_reason=spr.reject_reason,
    )

#возможно надо актуаизировать spr responce под новую таблицу маин и схемас

@app.post(
    "/spr/counter/accept",
    response_model=CounterActionResponse
)
def counter_accept(
    payload: CounterActionRequest,
    db: Session = Depends(get_db),
):
    return accept_counter(
        db=db,
        id=payload.id,
    )


@app.post(
    "/spr/counter/reject",
    response_model=CounterActionResponse
)
def counter_reject(
    payload: CounterActionRequest,
    db: Session = Depends(get_db),
):
    return reject_counter(
        db=db,
        id=payload.id,
        reason=payload.reason or "CLIENT_DECLINED",
    )
