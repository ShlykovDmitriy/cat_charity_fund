from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donations import donation_crud
from app.models import User
from app.schemas.donation import (DonationCreate, DonationGetForSuperuser,
                                  DonationGetForUser)
from app.services.investment import investment_service

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationGetForSuperuser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров. Возвращает список всех пожертвований."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationGetForUser,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Возвращает созданое пожертвование."""
    return await investment_service.create_donat(session, donation, user)


@router.get(
    '/my',
    response_model=List[DonationGetForUser],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    my_donations = await donation_crud.get_multi_donations_current_user(
        user=user, session=session)
    return my_donations
