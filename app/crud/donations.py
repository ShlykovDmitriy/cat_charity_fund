from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_multi_donations_current_user(
        self,
        user: User,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(Donation.user_id == user.id)
        )
        return db_obj.scalars().all()


donation_crud = CRUDDonation(Donation)
