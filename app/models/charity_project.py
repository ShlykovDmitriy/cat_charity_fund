from sqlalchemy import Column, String, Text

from app.core.constants import MAX_LEN_NAME_PROJECT
from app.models.base import BaseProjectDonationModel


class CharityProject(BaseProjectDonationModel):
    """Модель проекта, наследуется от базовой."""
    name = Column(String(MAX_LEN_NAME_PROJECT), unique=True, nullable=False)
    description = Column(Text, nullable=False)