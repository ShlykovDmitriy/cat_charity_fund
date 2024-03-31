from sqlalchemy import Column, String, Text

from app.models.base import BaseProjectDonationModel


class CharityProject(BaseProjectDonationModel):
    """Модель проекта, наследуется от базовой."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)