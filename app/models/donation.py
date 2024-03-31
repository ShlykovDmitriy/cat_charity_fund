from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseProjectDonationModel


class Donation(BaseProjectDonationModel):
    user_id = Column(Integer, ForeignKey('user.id', name='fk_donation_user_id_user'))
    comment = Column(Text)