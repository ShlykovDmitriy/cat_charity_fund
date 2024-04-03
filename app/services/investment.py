from datetime import datetime
from http import HTTPStatus
from typing import List, Union

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (FULL_AMOUNT_ERROR, INVESTED_AMOUNT_EXIST_ERROR,
                                PROJECT_CLOSE_ERROR, PROJECT_NAME_ERROR)
from app.crud.donations import donation_crud
from app.crud.projects import charity_project_crud
from app.models import CharityProject, Donation, User


class InvestmentService:

    async def _obj_not_fully_invested(
            self,
            model: Union[CharityProject, Donation],
            session: AsyncSession
    ) -> List[Union[Donation, CharityProject]]:
        objects = await session.execute(select(model).where(
            model.fully_invested.is_(False)
        ).order_by(model.create_date))
        return objects.scalars().first()

    async def _get_project_and_donation(
            self,
            obj: Union[CharityProject, Donation],
            session: AsyncSession
    ) -> tuple:
        """
        Функция получает переменные проекта и пожертвования.
        """
        if isinstance(obj, CharityProject):
            return obj, await self._obj_not_fully_invested(Donation, session)
        return await self._obj_not_fully_invested(CharityProject, session), obj

    async def _close_project_or_donation(
            self,
            obj_close: Union[CharityProject, Donation]
    ) -> None:
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
    ) -> Union[CharityProject, Donation]:
        """
        Функция инвестирования. Проверяет что есть пожертвования
        или проекты которые необходимо обработать.
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

    async def _name_charity_project_exist(
            self,
            name: str,
            session: AsyncSession,
    ) -> None:
        """Проверка на наличие имени."""
        charity_project = await charity_project_crud.found_charity_project_by_name(
            charity_project_name=name,
            session=session
        )
        if charity_project is not None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=PROJECT_NAME_ERROR
            )

    async def create_project(
            self,
            session: AsyncSession,
            charity_project: CharityProject
    ) -> CharityProject:
        """Создать проект."""
        await self._name_charity_project_exist(charity_project.name, session)
        project = await charity_project_crud.create(charity_project, session)
        return await self._create_investment(session, project)

    async def create_donat(
            self,
            session: AsyncSession,
            donation: Donation,
            user: User
    ) -> Donation:
        """Создать пожертвование."""
        donation = await donation_crud.create(donation, session, user)
        donation = await self._create_investment(session, donation)
        return donation

    async def _check_invested_amount_for_delete(
            self,
            project_id: int,
            session: AsyncSession
    ):
        """Проверка на наличие инвестиций."""
        charity_project = await charity_project_crud.get(project_id, session)
        if charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=INVESTED_AMOUNT_EXIST_ERROR
            )

    async def delete_project(
            self,
            charity_project: CharityProject,
            session: AsyncSession,
    ):
        """Удаляет проект. Нельзя удалить проект,
        в который уже были инвестированы средства."""

        await self._check_invested_amount_for_delete(
            charity_project.id, session)
        charity_project = await charity_project_crud.remove(
            charity_project, session
        )
        return charity_project

    async def _check_fully_invested_for_update(
            self,
            project_id: int,
            session: AsyncSession,
    ) -> None:
        """Проверка, что проект не закрыт."""
        charity_project = await charity_project_crud.get(project_id, session)
        if charity_project.fully_invested:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=PROJECT_CLOSE_ERROR
            )

    async def _check_full_amount_for_update(
            self,
            project_id: int,
            obj_in_full_amount,
            session: AsyncSession,
    ) -> None:
        """
        Проверка измененного значения full_amount.
        Не должно быть меньше вложеных пожертвований.
        """
        charity_project = await charity_project_crud.get(project_id, session)
        if obj_in_full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=FULL_AMOUNT_ERROR
            )

    async def update_project(
            self,
            charity_project: CharityProject,
            obj_in: CharityProject,
            session: AsyncSession,
    ) -> CharityProject:
        """Закрытый проект нельзя редактировать;
        нельзя установить требуемую сумму меньше уже вложенной."""
        await self._check_fully_invested_for_update(
            charity_project.id, session)
        if obj_in.name:
            await self._name_charity_project_exist(obj_in.name, session)
        if obj_in.full_amount:
            await self._check_full_amount_for_update(
                charity_project.id, obj_in.full_amount, session)
        return await charity_project_crud.update(
            charity_project, obj_in, session)


investment_service = InvestmentService()
