from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import PROJECT_NO_FOUND_ERROR
from app.crud.projects import charity_project_crud
from app.models import CharityProject


async def get_project_or_404(
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
            detail=PROJECT_NO_FOUND_ERROR
        )
    return charity_project
