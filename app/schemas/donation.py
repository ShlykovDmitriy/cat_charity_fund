from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationGetForUser(DonationCreate):
    id: Optional[int]
    create_date: datetime

    class Config:
        orm_mode = True


class DonationGetForSuperuser(DonationGetForUser):
    user_id: int
    invested_amount: Optional[int] = Field(default=0)
    fully_invested: Optional[bool] = Field(default=False)
    close_date: Optional[datetime]
