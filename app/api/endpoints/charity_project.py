from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_can_be_deleted,
    check_project_can_be_updated,
    check_project_exists,
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investing import invest_new_project


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/', response_model=list[CharityProjectDB], summary="Получить проекты"
)
async def get_all_charity_projects(session: SessionDep):
    """Показать список всех целевых проектов."""
    return await charity_project_crud.get_multi(session)


@router.post('/', response_model=CharityProjectDB, summary="Создать проект")
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: SessionDep,
):
    """Создать целевой проект."""
    await check_name_duplicate(project_in.name, session)
    new_project = CharityProject(**project_in.model_dump())
    return await invest_new_project(new_project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary="Редактировать проект"
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep,
):
    """
    Редактировать целевой проект.

    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await check_project_exists(project_id, session)
    check_project_can_be_updated(project, obj_in)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    return await charity_project_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}', response_model=CharityProjectDB, summary="Удалить проект"
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
):
    """
    Удалить целевой проект.

    Нельзя удалить проект, в который уже были инвестированы средства.
    """
    project = await check_project_exists(project_id, session)
    check_project_can_be_deleted(project)
    return await charity_project_crud.remove(project, session)