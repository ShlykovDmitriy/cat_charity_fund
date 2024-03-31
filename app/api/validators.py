from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.projects import charity_project_crud
from app.models.charity_project import CharityProject


async def charity_project_exist(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка на наличие проекта."""
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект не найден.'
        )
    return charity_project


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
            detail='Проект с таким именем уже существует!'
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
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_full_amount_for_update(
        project_id: int,
        obj_in_full_amount,
        session: AsyncSession,
) -> CharityProject:
    """
    Проверка измененного значения full_amount.
    Не должно быть меньше вложеных пожертвований.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if obj_in_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Требуемая сумма проекта не может быть меньше вложенной!',
        )
    return charity_project


async def check_fully_invested_for_update(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка, что проект не закрыт."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя изменять закрытый проект.',
        )
    return charity_project
