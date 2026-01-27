from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import schemas
import service
from clients import call_spr, call_spr_counter_accept, call_spr_counter_reject
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Application Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# DB init
# =====================================================
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================================
# CREATE APPLICATION
# =====================================================
@app.post("/applications", response_model=schemas.ApplicationResponse)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
):
    # 1. создаём заявку
    created_app = service.create_application(db, application)

    # 2. payload в SPR
    spr_payload = {
        "id": created_app.id,
        "client_id": created_app.client_id,
        "first_name": created_app.first_name,
        "last_name": created_app.last_name,
        "middle_name": created_app.middle_name,
        "birth_date": created_app.birth_date.isoformat(),
        "loyal_client": 0,
        "successful_loans_count": 0,
        "passport_number": created_app.passport_number,
        "phone_number": created_app.phone_number,
        "requested_amount": created_app.requested_amount,
        "requested_days": created_app.requested_days,
    }

    # 3. вызов SPR
    try:
        spr_result = call_spr(spr_payload)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"SPR service error: {str(e)}"
        )

    # 4. единый ответ (Application + SPR)
    return {
        "id": created_app.id,
        "client_id": created_app.client_id,

        "requested_amount": created_app.requested_amount,
        "requested_days": created_app.requested_days,

        **spr_result
    }

@app.post("/applications/{id}/counter/accept")
def accept_application_counter(id: int):
    return call_spr_counter_accept({"id": id})


@app.post("/applications/{id}/counter/reject")
def reject_application_counter(id: int, reason: str = "CLIENT_DECLINED"):
    return call_spr_counter_reject({
        "id": id,
        "reason": reason,
    })
