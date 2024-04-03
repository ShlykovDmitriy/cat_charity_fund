from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import name_charity_project_exist
from app.crud.donations import donation_crud
from app.crud.projects import charity_project_crud
from app.models import CharityProject, Donation, User


class InvestmentService:

    async def _obj_not_fully_invested(
            self,
            model: Union[CharityProject, Donation],
            session: AsyncSession
    ):
        objects = await session.execute(select(model).where(
            model.fully_invested.is_(False)
        ).order_by(model.create_date))
        return objects.scalars().first()

    async def _get_project_and_donation(
            self,
            obj: Union[CharityProject, Donation],
            session: AsyncSession
    ):
        """
        Функция получает переменные проекта и пожертвования.
        """
        if isinstance(obj, CharityProject):
            return obj, await self._obj_not_fully_invested(Donation, session)

        elif isinstance(obj, Donation):
            return await self._obj_not_fully_invested(CharityProject, session), obj

    async def _close_project_or_donation(
            self,
            obj_close: Union[CharityProject, Donation]
    ):
        """
        Функция меняет значение fully_invested на True
        и подставляет дату закрытия.
        """
        obj_close.fully_invested = True
        obj_close.close_date = datetime.now()

    async def _create_investment(
            self,
            session: AsyncSession,
            obj: Union[CharityProject, Donation],
    ):
        """
        Функция инвестирования.
        Проверяет что есть пожертвования или проекты которые необходимо обработать.
        Распределяет пожертования по проектам начиная с самого первого.
        """

        project, donation = await self._get_project_and_donation(obj, session)

        if not project or not donation:
            await session.commit()
            await session.refresh(obj)
            return obj

        amount_project = project.full_amount - project.invested_amount
        amount_donation = donation.full_amount - donation.invested_amount

        if amount_project > amount_donation:
            project.invested_amount += amount_donation
            donation.invested_amount += amount_donation
            await self._close_project_or_donation(donation)

        else:
            project.invested_amount += amount_project
            donation.invested_amount += amount_project
            await self._close_project_or_donation(project)
            if amount_project == amount_donation:
                await self._close_project_or_donation(donation)

        session.add(project)
        session.add(donation)
        await session.commit()
        await session.refresh(project)
        await session.refresh(donation)
        if donation.fully_invested if isinstance(obj, CharityProject) else project.fully_invested:
            await self._create_investment(session, obj)
        return obj

    async def create_project(
            self,
            session: AsyncSession,
            charity_project: CharityProject
    ):
        """Создать проект."""
        await name_charity_project_exist(charity_project.name, session)
        project = await charity_project_crud.create(charity_project, session)
        return await self._create_investment(session, project)

    async def create_donat(
            self,
            session: AsyncSession,
            donation: Donation,
            user: User
    ):
        """Создать пожертвование."""
        donation = await donation_crud.create(donation, session, user)
        donation = await investment_service._create_investment(session, donation)
        return donation


investment_service = InvestmentService()
