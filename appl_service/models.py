from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    client_id = Column(String, nullable=False)

    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String, nullable=True)
    birth_date = Column(Date)

    passport_number = Column(String)
    phone_number = Column(String)

    requested_amount = Column(Integer)
    requested_days = Column(Integer)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
