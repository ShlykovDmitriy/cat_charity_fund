from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utilits import get_project_or_404
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.projects import charity_project_crud
from app.schemas.charityproject import ProjectCreate, ProjectDB, ProjectUpdate
from app.services.investment import investment_service

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
    """Только для суперюзеров. Вернет созданный проект."""
    return await investment_service.create_project(session, charity_project)


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
    charity_project = await get_project_or_404(project_id, session)
    return await investment_service.delete_project(charity_project, session)


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
    charity_project = await get_project_or_404(project_id, session)
    return await investment_service.update_project(
        charity_project, obj_in, session)
