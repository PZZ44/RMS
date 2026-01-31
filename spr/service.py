from sqlalchemy.orm import Session
from sqlalchemy import func, text

from models import SPR, SPRScore
from schemas import ApplicationData
from clients import call_risk_service, call_bki, call_sim
from datetime import datetime, date


# score_min, score_max, product_type, base_limit
RISK_BANDS = [
    (0, 19,  "Very High", 0),
    (20, 29, "Toy",       1000),
    (30, 49, "High",      5000),
    (50, 69, "Medium",   15000),
    (70, 100,"Low",      30000),
]


def get_risk_band(score: int):
    for min_s, max_s, band, limit in RISK_BANDS:
        if min_s <= score <= max_s:
            return band, limit
    return "Very High", 0


# score_min, score_max, decision, penalty
BKI_BANDS = [
    (0,   449, "HARD_REJECT", None),
    (450, 499, "PENALTY", -50),
    (500, 549, "PENALTY", -25),
    (550, 599, "PENALTY", -10),
    (600, 999, "OK", 0),
]


def apply_bki(score: int, bki_score: int):
    for min_s, max_s, action, penalty in BKI_BANDS:
        if min_s <= bki_score <= max_s:
            if action == "HARD_REJECT":
                return score, True, "BKI_BELOW_450"
            return score + penalty, False, None
    return score, False, None


# score_min, score_max, penalty
SIM_LIFETIME_BANDS = [
    (0, 0, -50),
    (1, 1, -20),
    (2, 2, -10),
    (3, 5, 0),
]

# score_min, score_max, penalty
SIM_CLC_BANDS = [
    (0, 0, -25),
    (1, 1, -15),
    (2, 2, -5),
    (3, 5, 0),
]


def _apply_band(value: int, bands):
    for min_v, max_v, penalty in bands:
        if min_v <= value <= max_v:
            return penalty
    return 0


def apply_sim(score: int, lifetime: int, clc: int):
    score += _apply_band(lifetime, SIM_LIFETIME_BANDS)
    score += _apply_band(clc, SIM_CLC_BANDS)
    return score



def loans_multiplier(loan_num: int) -> float:
    if loan_num <= 1:
        return 1.0
    if loan_num <= 3:
        return 1.2
    if loan_num <= 5:
        return 1.4
    return 1.5


def normalize_score(score: int) -> int:
    return max(0, min(score, 100))


def generate_agr_number(db: Session) -> str:
    seq = db.execute(text("SELECT nextval('agr_number_seq')")).scalar()
    year = datetime.now().year
    return f"ВВ-{year}/{seq:06d}"


def calculate_age(birth_date_str: str) -> int:
    birth_date = date.fromisoformat(birth_date_str)
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )

def _reject(
    db: Session,
    data: ApplicationData,
    loyal_client: int,
    score: int,
    reason: str,
) -> SPR:
    spr = SPR(
        id=int(data.id),
        client_id=data.client_id,
        loyal_client=loyal_client,
        decision="REJECT",
        status="CLOSED",
        final_score=score,
        risk_band=None,
        approved_amount=None,
        approved_days=None,
        reject_reason=reason,
    )

    db.add(spr)
    db.flush()
    return spr

# Автоотказ если клиент не принял оффер в течении 24 часов.

def expire_counters(db: Session):
    expired = (
        db.query(SPR)
        .filter(
            SPR.decision == "COUNTER",
            SPR.status == "OPEN",
            SPR.created_at < func.now() - text("interval '24 hours'")
        )
        .all()
    )

    for spr in expired:
        spr.decision = "REJECT"
        spr.status = "CLOSED"
        spr.reject_reason = "COUNTER_EXPIRED"

    db.commit()

    return len(expired)


# MAIN DECISION

def make_decision(db: Session, data: ApplicationData):
    """
    Полный decision pipeline SPR

    APPROVED — создаётся договор
    COUNTER  — сохранённое предложение, без договора
    REJECT   — финальный отказ
    """

    with db.begin():

        approved_loans = (
            db.query(func.count(SPR.id))
            .filter(
                SPR.client_id == data.client_id,
                SPR.decision == "APPROVED",
            )
            .scalar()
        )

        loyal_client = 1 if approved_loans > 0 else 0

        score = 100 if loyal_client == 1 else 90


        # RISK
        age = calculate_age(data.birth_date)

        risk = call_risk_service({
            "age": age,
            "loyal_client": loyal_client,
            "successful_loans_count": approved_loans,
        })

        if risk["hard_reject"]:
            spr = _reject(
                db=db,
                data=data,
                loyal_client=loyal_client,
                score=0,
                reason=risk["reject_reason"],
            )
            return spr, "REJECT"

        score -= risk["penalties"]

        # BKI
        bki = call_bki({
            "first_name": data.first_name,
            "last_name": data.last_name,
            "middle_name": data.middle_name,
            "birth_date": data.birth_date,
            "passport_number": data.passport_number,
        })

        score, hard_reject, reason = apply_bki(score, bki["bki_score"])

        if hard_reject:
            spr = _reject(
                db=db,
                data=data,
                loyal_client=loyal_client,
                score=score,
                reason=reason,
            )
            return spr, "REJECT"

        # SIM
        sim = call_sim({
            "first_name": data.first_name,
            "last_name": data.last_name,
            "middle_name": data.middle_name,
            "birth_date": data.birth_date,
            "phone_number": data.phone_number,
        })

        score = apply_sim(score, sim["lifetime"], sim["clc"])
        score = normalize_score(score)

        # DECISION
        risk_band, base_limit = get_risk_band(score)

        limit = int(base_limit * loans_multiplier(approved_loans + 1))

        if base_limit == 0:
            spr = _reject(
                db=db,
                data=data,
                loyal_client=loyal_client,
                score=score,
                reason="LOW_SCORE",
            )
            return spr, "REJECT"

        if data.requested_amount <= limit:
            decision = "APPROVED"
            approved_amount = data.requested_amount
            status = "ISSUED"
        else:
            decision = "COUNTER"
            approved_amount = limit
            status = "OPEN"

        approved_days = data.requested_days


        spr = SPR(
            id=int(data.id),
            client_id=data.client_id,
            loyal_client=loyal_client,
            decision=decision,
            status=status,
            final_score=score,
            risk_band=risk_band,
            approved_amount=approved_amount,
            approved_days=approved_days,
        )

        db.add(spr)
        db.flush()  

        if decision == "APPROVED":
            spr.loan_num = approved_loans + 1
            spr.agr_number = generate_agr_number(db)

        # SCORES SAVING
        db.add_all([
            SPRScore(
                id=data.id,
                source="RISK",
                score_type="penalties",
                score_value=risk["penalties"],
            ),
            SPRScore(
                id=data.id,
                source="BKI",
                score_type="bki_score",
                score_value=bki["bki_score"],
            ),
            SPRScore(
                id=data.id,
                source="SIM",
                score_type="lifetime",
                score_value=sim["lifetime"],
            ),
            SPRScore(
                id=data.id,
                source="SIM",
                score_type="clc",
                score_value=sim["clc"],
            ),
        ])

        return spr, decision

