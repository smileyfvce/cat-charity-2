from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
    name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!',
        )
    return project


def check_project_can_be_updated(
    project: CharityProject,
    obj_in: CharityProjectUpdate,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if (
        obj_in.full_amount is not None and
        obj_in.full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нелья установить значение full_amount '
                'меньше уже вложенной суммы.'
            ),
        )


def check_project_can_be_deleted(project: CharityProject) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )