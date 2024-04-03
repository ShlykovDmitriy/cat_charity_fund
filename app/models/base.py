from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.constants import DEFAULT_INVESTED_AMOUNT
from app.core.db import Base


class BaseProjectDonationModel(Base):
    """Базовая абстрактная модель."""
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
