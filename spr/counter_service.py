from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from models import SPR
from service import generate_agr_number
from database import get_db

from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import SPR
from service import generate_agr_number


def accept_counter(
    db: Session,
    id: int,
):
    spr = (
        db.query(SPR)
        .filter(SPR.id == id)
        .one_or_none()
    )

    if not spr:
        raise HTTPException(status_code=404, detail="SPR not found")

    # ✅ ИДЕМПОТЕНТНОСТЬ
    if spr.decision == "APPROVED" and spr.status == "ISSUED":
        return {
            "id": spr.id,
            "decision": "APPROVED",
            "approved_amount": spr.approved_amount,
            "approved_days": spr.approved_days,
            "agr_number": spr.agr_number,
        }

    if spr.decision != "COUNTER" or spr.status != "OPEN":
        raise HTTPException(
            status_code=409,
            detail="Counter offer is not active"
        )

    # ===== финализация =====
    spr.decision = "APPROVED"
    spr.status = "ISSUED"

    spr.loan_num = (
        db.query(SPR)
        .filter(
            SPR.client_id == spr.client_id,
            SPR.decision == "APPROVED",
        )
        .count()
        + 1
    )

    spr.agr_number = generate_agr_number(db)

    db.commit()

    return {
        "id": spr.id,
        "decision": "APPROVED",
        "approved_amount": spr.approved_amount,
        "approved_days": spr.approved_days,
        "agr_number": spr.agr_number,
    }



def reject_counter(
    db: Session,
    id: int,
    reason: str,
):
    spr = db.query(SPR).filter(SPR.id == id).one_or_none()

    if not spr:
        raise HTTPException(status_code=404, detail="SPR not found")

    # ✅ ИДЕМПОТЕНТНОСТЬ
    if spr.decision == "REJECT" and spr.status == "CLOSED":
        return {
            "id": spr.id,
            "decision": "REJECT",
            "reject_reason": spr.reject_reason,
        }

    if spr.decision != "COUNTER" or spr.status != "OPEN":
        raise HTTPException(
            status_code=409,
            detail="Counter offer is not active"
        )

    spr.decision = "REJECT"
    spr.status = "CLOSED"
    spr.reject_reason = reason

    db.commit()

    return {
        "id": spr.id,
        "decision": "REJECT",
        "reject_reason": spr.reject_reason,
    }
