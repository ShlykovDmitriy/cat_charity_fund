from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (charity_project_exist,
                                check_full_amount_for_update,
                                check_fully_invested_for_update,
                                check_invested_amount_for_delete,
                                name_charity_project_exist)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.projects import charity_project_crud
from app.schemas.charityproject import (ProjectDB, ProjectCreate,
                                        ProjectUpdate)
from app.services.investment import create_investment

router = APIRouter()


@router.get(
    '/',
    response_model=List[ProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    """Возвращает список всех проектов."""
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=ProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        charity_project: ProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Создаёт благотворительный проект."""
    await name_charity_project_exist(charity_project.name, session)
    project = await charity_project_crud.create(charity_project, session)
    project = await create_investment(session, project)
    return project


@router.delete(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть."""
    charity_project = await charity_project_exist(project_id, session)
    await check_invested_amount_for_delete(charity_project.id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: ProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной."""
    charity_project = await charity_project_exist(project_id, session)
    await check_fully_invested_for_update(project_id, session)
    if obj_in.name:
        await name_charity_project_exist(obj_in.name, session)
    if obj_in.full_amount:
        await check_full_amount_for_update(
            project_id, obj_in.full_amount, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
