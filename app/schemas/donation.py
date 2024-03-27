from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Extra


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class MyDonationGet(DonationCreate):
    id: int
    create_date: datetime


class AllDonationGet(MyDonationGet):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
