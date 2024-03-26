from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Boolean, DateTime, Integer, String, Text, ForeignKey

from app.core.db import Base


class BaseProjectDonationModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=lambda: datetime.utcnow().strftime("%d.%m.%Y-%H%M%S"))
    close_date = Column(DateTime)


class CharityProject(BaseProjectDonationModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)


class Donation(BaseProjectDonationModel):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
