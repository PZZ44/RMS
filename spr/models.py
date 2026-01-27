from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func

from database import Base


class SPR(Base):
    __tablename__ = "spr"

    # === Технический PK решения ===
    id = Column(Integer, primary_key=True)

    # === Клиент ===
    client_id = Column(String, nullable=False)

    # === Договор ===
    agr_number = Column(String, unique=True, nullable=True)
    loan_num = Column(Integer, nullable=False)

    # === Состояние клиента ===
    loyal_client = Column(Integer, nullable=False)  # 0 / 1

    # === Итоговое решение ===
    final_score = Column(Integer, nullable=False)
    risk_band = Column(String, nullable=False)

    approved_amount = Column(Integer, nullable=True)
    approved_days = Column(Integer, nullable=True)

    decision = Column(String, nullable=False)      # APPROVED / COUNTER / REJECT
    status = Column(String, nullable=False)        # OPEN / ISSUED / DECLINED / CLOSED

    reject_reason = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class SPRScore(Base):
    __tablename__ = "spr_scores"
    
    scoring_id = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False, index=True)
    # === Источник и тип скора ===
    source = Column(String, nullable=False)        # BKI / SIM / RISK
    score_type = Column(String, nullable=False)    # main / lifetime / clc / penalty
    score_value = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
