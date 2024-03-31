from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.constants import (MAX_LEN_NAME_PROJECT,
                                MIN_LEN_DESCRIPTION_PROJECT,
                                MIN_LEN_NAME_PROJECT)


class ProjectCreate(BaseModel):
    """Схема для создания проекта."""
    name: str = Field(
        ..., min_length=MIN_LEN_NAME_PROJECT, max_length=MAX_LEN_NAME_PROJECT)
    description: str = Field(
        ..., min_length=MIN_LEN_DESCRIPTION_PROJECT)
    full_amount: PositiveInt


class ProjectUpdate(BaseModel):
    """Схема для изменения проекта."""
    name: Optional[str] = Field(
        None, min_length=MIN_LEN_NAME_PROJECT, max_length=MAX_LEN_NAME_PROJECT)
    description: Optional[str] = Field(
        None, min_length=MIN_LEN_DESCRIPTION_PROJECT)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class ProjectDB(ProjectCreate):
    """Схема для показа проекта/ов."""
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
