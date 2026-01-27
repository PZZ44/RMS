#!/usr/bin/env python3

from datetime import datetime, timedelta
from database import SessionLocal
from models import SPR
from sqlalchemy import update

def run():
    db = SessionLocal()

    try:
        expire_before = datetime.utcnow() - timedelta(hours=24)

        stmt = (
            update(SPR)
            .where(
                SPR.decision == "COUNTER",
                SPR.status == "OPEN",
                SPR.created_at < expire_before,
            )
            .values(
                decision="REJECT",
                status="CLOSED",
                reject_reason="COUNTER_EXPIRED",
            )
        )

        result = db.execute(stmt)
        db.commit()

        print(f"Expired counters: {result.rowcount}")

    finally:
        db.close()
