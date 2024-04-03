from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (FULL_AMOUNT_ERROR, INVESTED_AMOUNT_EXIST_ERROR,
                                PROJECT_CLOSE_ERROR, PROJECT_NAME_ERROR)
from app.crud.projects import charity_project_crud
from app.models.charity_project import CharityProject


async def name_charity_project_exist(
    name: str,
    session: AsyncSession,
):
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


async def check_invested_amount_for_delete(
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


async def check_full_amount_for_update(
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


async def check_fully_invested_for_update(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка, что проект не закрыт."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_CLOSE_ERROR
        )
    return charity_project
