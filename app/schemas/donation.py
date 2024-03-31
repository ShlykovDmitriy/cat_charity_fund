from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationCreate(BaseModel):
    """Схема для создания пожертвований."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationGetForUser(DonationCreate):
    """Схема для показа пожертований. Для пользователей."""
    id: Optional[int]
    create_date: datetime

    class Config:
        orm_mode = True


class DonationGetForSuperuser(DonationGetForUser):
    """Схема для показа пожертований. Для суперпользователей."""
    user_id: int
    invested_amount: Optional[int] = Field(default=0)
    fully_invested: Optional[bool] = Field(default=False)
    close_date: Optional[datetime]
